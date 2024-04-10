from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class EmailUser(AbstractUser):
    first_name = models.CharField(max_length=120, blank=True)
    email_prefix = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField()
    first_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


STATUS_CHOICES = (
    ('Rec', 'received'),
    ('Rd', 'read'),
    ('Arch', 'archived'),
)


# User = get_user_model()


class Message(models.Model):
    from_whom = models.ForeignKey(EmailUser, on_delete=models.CASCADE, related_name='sent_messages')
    to_whom = models.ForeignKey(EmailUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
