from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.user.username


class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ('topup', 'Top Up'),
        ('sms', 'SMS Deduction'),
    ]

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    reference = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.transaction_type