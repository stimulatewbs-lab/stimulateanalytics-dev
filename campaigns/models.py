from django.db import models
from contacts.models import ContactGroup


class Campaign(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
    ]

    name = models.CharField(
        max_length=255
    )

    message = models.TextField()

    target_groups = models.ManyToManyField(
        ContactGroup,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name