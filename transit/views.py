from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import DriveForm, ApplicationForm, AccountForm, UserForm, MessageForm
from .models import Drive, Notification, Application
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    context={}
    return render(request,'transit/home.html', context)


def new_drive(request):
    form = DriveForm
    if request.method == 'POST':
        form = DriveForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_of_drives')
    context={
        'form':form
    }

    return render(request,'transit/new_drive.html', context)

def list_of_drives(request):
    sort_option = request.GET.get('sort', 'default') 

    if sort_option == 'high_to_low':
        drives = Drive.objects.order_by('-price')
    elif sort_option == 'low_to_high':
        drives = Drive.objects.order_by('price')
    else:
        drives = Drive.objects.all()

    context = {'drives': drives, 'sort_option': sort_option}
    context={
        'drives':drives
    }
    return render(request,'transit/list_of_drives.html', context)

def detail(request, drive_id):
    drive = get_object_or_404(Drive, pk=drive_id)
    user = request.user
    form = ApplicationForm()

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = user
            application.drive = drive
            application.save()

            Notification.objects.create(
                sender=user,  
                receiver=drive.driver.account.user,  
                title="New Application",
                text=f"New application for your drive: {drive.title}",
            )

            Notification.objects.create(
                sender=user,
                receiver=user,
                title="Application Submitted",
                text=f"Your application for the drive {drive.title} has been submitted successfully.",
            )

            messages.success(request, 'Application successfully submitted.')
            return redirect('user_dashboard')

    context = {
        'drive': drive,
        'form': form,
        'user': user
    }

    return render(request, 'transit/detail.html', context)


def singup_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)
        context={
            'form1':user_form,
            'form2': account_form
        }
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            account = account_form.save(commit=False)
            account.user = user
            account.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'registration/singup.html', context)
    else:
        user_form = UserForm()
        account_form = AccountForm()
    context={
        'form1':user_form,
        'form2': account_form
    }
    return render(request,'registration/singup.html',context)


@login_required
def user_dashboard(request):
    user = request.user
    my_applications = user.application_set.all()
    accepted_applications = my_applications.filter(accepted=True)
    completed_applications = [application for application in accepted_applications if application.drive.has_date_passed()]
    context={
        'my_applications':my_applications,
        'completed_applications':completed_applications,
        'user':user
    }
    return render(request,'accounts/dashboard.html',context)

@login_required
def driver_dashboard(request):
    user = request.user
    my_drives = user.drive_set.all()
    applications_for_my_drives = Application.objects.filter(drive__in=my_drives)
    
    context = {
        'user': user,
        'applications_for_my_drives': applications_for_my_drives,
        'drives' : my_drives,
    }
    return render(request, 'accounts/driver_dashboard.html', context)


def set_status(request, drive_id):
    drive = get_object_or_404(Drive, id=drive_id)
    if drive.status == "Active":
        drive.status = 'Unactive'
    else:
        drive.status = 'Active'
    drive.save()
    return redirect('driver_dashboard')

def accept_drive_and_change_seats(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    drive = application.drive
    drive.accept_drive(application)
    drive.change_number_of_seats(application)

    sender = request.user 
    receiver = application.user  
    title = "Request accepted"
    text = f"Your request is accepted for drive: {drive.title}"
    
    notification = Notification.objects.create(
        sender=sender,
        receiver=receiver,
        title=title,
        text=text
    )
    return redirect('driver_dashboard')

@login_required
def profile(request):
    user = request.user
    received_notifications = Notification.objects.filter(receiver=user).order_by('-sent_at')
    context={
        'user': user,
        'notifications': received_notifications
    }
    return render(request,'accounts/profile.html',context)