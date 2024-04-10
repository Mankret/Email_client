from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, Textarea, EmailInput, PasswordInput
from email_client.models import EmailUser

# User = get_user_model()


class RegistrationForm(UserCreationForm):
    email_prefix = forms.CharField(max_length=100, label='Enter your email prefix')
    # password = forms.CharField(widget=forms.PasswordInput())
    # confirm_password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=100, required=False)

    class Meta:
        model = EmailUser
        fields = ["first_name", "username", "contact_email", "email_prefix"]
