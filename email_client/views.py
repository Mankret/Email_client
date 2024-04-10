from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from email_client.forms import RegistrationForm
from email_client.models import Message, EmailUser

user = get_user_model()


def home(request):
    print('home is here')
    return render(request, 'home.html')


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email_prefix = form.cleaned_data.get('email_prefix')
        contact_email = form.cleaned_data.get('contact_email')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        email_p = f"{email_prefix}@mankretmail.com"

        user = EmailUser.objects.create_user(username=username, email=contact_email, password=password,
                                             email_prefix=email_p)
        # user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class InMailBox(generic.ListView):
    modes = Message
    template_name = 'registration/inmailbox.html'

    def get_queryset(self):
        print('something')
        return Message.objects.select_related('to_whom').filter(to_whom_id=self.request.user.id)
