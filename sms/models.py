from django.db import models
from contacts.models import Contact
from campaigns.models import Campaign


class SMSMessage(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.contact.phone_number} - {self.status}"