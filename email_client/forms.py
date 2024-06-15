from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, Textarea, EmailInput, PasswordInput
from email_client.models import EmailUser, Message



class RegistrationForm(UserCreationForm):
    email_prefix = forms.CharField(max_length=100, label='Enter your email prefix')
    username = forms.CharField(max_length=100, required=False)

    class Meta:
        model = EmailUser
        fields = ["first_name", "username", "contact_email", "email_prefix"]


class MessageSendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['to_whom', 'subject', 'content']
        widgets = {
            'to_whom': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }