from django.db import models
from django.conf import settings
from campaigns.models import Campaign
from contacts.models import Contact


class SMSMessage(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE
    )

    sender_id = models.CharField(max_length=20)

    phone = models.CharField(max_length=20)

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    gateway_message_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    sent_at = models.DateTimeField(
        blank=True,
        null=True
    )

    delivered_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.phone
    from django.db import models

class Campaign(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name