from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from transit.forms import MessageForm

def messenger(request):
    user = request.user
    my_conversations = Message.get_all_conversations(user)
    my_user = my_conversations.first()
    return HttpResponseRedirect(reverse('messenger:messages_from_conversations', args=[my_user.id]))


@login_required
def messages_from_conversations(request, user_id=None):
    user = request.user
    my_conversations = Message.get_all_conversations(user)
    other_user, all_messages = None, None

    form = MessageForm()
    if user_id:
        other_user = get_object_or_404(User, pk=user_id)
        all_messages = Message.get_all_messages(user, other_user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.m_sender = request.user
            message.m_receiver = form.cleaned_data['receiver']
            message.save()
    else:
        form = MessageForm()
    context = {
        'my_conversations': my_conversations,
        'other_user': other_user,
        'all_messages': all_messages,
        'form':form
    }

    return render(request, 'messenger/messenger.html', context)

