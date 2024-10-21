from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput, PasswordInput,NullBooleanSelect
from django.forms import ModelForm
from .models import Drive,Application, Account
from messenger.models import Message

class DriveForm(forms.ModelForm):
    class Meta:
        model = Drive
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control orange-input', 'placeholder': 'Naziv vožnje'}),
            'price': forms.NumberInput(attrs={'class': 'form-control orange-input', 'placeholder': 'Cijena'}),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control grey-input', 'placeholder': 'Datum i vrijeme'}),
            'image': forms.FileInput(attrs={'class': 'form-control orange-input', 'accept': 'image/*', 'placeholder': 'Odaberite sliku'}),
        }

class ApplicationForm(ModelForm):
     
    class Meta:
        model = Application
        fields = ['seats']
        widgets = {
            'seats': forms.NumberInput(attrs={'class': 'form-control orange-input'}),
        }
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class AccountForm(ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    driver = forms.BooleanField(
        label="Driver",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Account
        fields = ['name', 'driver']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
        }

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), label='Receiver', widget=forms.Select)

    class Meta:
        model = Message
        fields = ['receiver', 'text']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'})