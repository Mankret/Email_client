from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse


class EmailUser(AbstractUser):
    first_name = models.CharField(max_length=120, blank=True)
    email_prefix = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField()
    first_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    STATUS_CHOICES = (
        ('Rec', 'received'),
        ('Rd', 'read'),
        ('Arch', 'archived'),
    )

    from_whom = models.EmailField(max_length=254)
    to_whom = models.EmailField(max_length=254)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Rec')
    is_deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('message-detail', args=[str(self.pk)])

    def __str__(self):
        return self.subject
