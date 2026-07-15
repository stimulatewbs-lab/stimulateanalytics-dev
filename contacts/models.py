from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.first_name


class ContactGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    contacts = models.ManyToManyField(
        Contact,
        blank=True,
        related_name="groups"
    )

    def __str__(self):
        return self.name