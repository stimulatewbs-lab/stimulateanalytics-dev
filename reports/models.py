from django.db import models
from sms.models import SMSMessage


class DeliveryReport(models.Model):

    sms = models.OneToOneField(
        SMSMessage,
        on_delete=models.CASCADE
    )

    delivery_status = models.CharField(
        max_length=50
    )

    gateway_response = models.TextField()

    delivered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.delivery_status