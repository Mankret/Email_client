from django.contrib import admin

from email_client.models import Message, EmailUser

admin.site.register(Message)
admin.site.register(EmailUser)
