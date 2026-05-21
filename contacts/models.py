from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class ContactGroup(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contact(models.Model):

    group = models.ForeignKey(ContactGroup, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, blank=True)

    phone = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone