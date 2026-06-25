from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=100)

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True
    )

    email = models.EmailField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.phone_number


class ContactGroup(models.Model):
    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=255)

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name