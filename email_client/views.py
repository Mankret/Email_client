import logging
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from email_client.forms import RegistrationForm, MessageSendForm
from email_client.models import Message, EmailUser
from email_client.task import send_email_task

user = get_user_model()

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            email_prefix = form.cleaned_data.get('email_prefix')
            contact_email = form.cleaned_data.get('contact_email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            email_p = f"{email_prefix}@mankretmail.com"

            user = EmailUser.objects.create_user(username=username, email=contact_email, password=password,
                                                 email_prefix=email_p)
            user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
            login(self.request, user)
            logger.info(f'User {username} registered and logged in successfully.')
            return super(RegisterFormView, self).form_valid(form)
        except Exception as e:
            logger.error(f'Registration failed: {e}')
            return super(RegisterFormView, self).form_valid(form)


class InMailBox(generic.ListView):
    modes = Message
    template_name = 'registration/inmailbox.html'
    context_object_name = 'inbox_messages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent_messages'] = Message.objects.filter(from_whom=self.request.user.email, is_deleted=False).order_by(
            '-timestamp')
        return context

    def get_queryset(self):
        return Message.objects.filter(to_whom=self.request.user.email, is_deleted=False).order_by('-timestamp')


class SendMessageView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageSendForm
    template_name = 'registration/sending_form.html'
    success_url = reverse_lazy('inbox')

    def form_valid(self, form):
        try:
            form.instance.from_whom = self.request.user
            form.instance.status = 'Rec'
            logger.debug(f'Form data: {form.cleaned_data}')

            response = super().form_valid(form)

            to_email = form.cleaned_data.get('to_whom')
            subject = form.cleaned_data.get('subject')
            content = form.cleaned_data.get('content')

            send_email_task.delay(subject, content, self.request.user.email, [to_email])

            logger.info(
                f'Message from {self.request.user.email} to {form.instance.to_whom} saved successfully and email sent.')

            return response
        except Exception as e:
            logger.error(f'Sending message failed: {e}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.error(f'Form errors: {form.errors}')
        return super().form_invalid(form)


class MessageDetailView(generic.DetailView):
    model = Message
    context_object_name = 'message'

    def render_to_response(self, context, **response_kwargs):
        try:
            message = context['message']
            data = {
                'from_who': message.from_who,
                'subject': message.subject,
                'body': message.body,
            }
            logger.debug(f'Message detail viewed: {data}')
            return JsonResponse(data)
        except Exception as e:
            logger.error(f'Error rendering message detail: {e}')
            return JsonResponse({'error': str(e)}, status=500)
