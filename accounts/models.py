import hashlib
import secrets

from django.conf import settings
from django.db import models
from django.utils import timezone


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
    )

    is_phone_verified = models.BooleanField(
        default=False,
    )

    is_email_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.user.username


class OTPVerification(models.Model):
    CHANNEL_EMAIL = "email"
    CHANNEL_SMS = "sms"

    CHANNEL_CHOICES = [
        (CHANNEL_EMAIL, "Email"),
        (CHANNEL_SMS, "SMS"),
    ]

    PURPOSE_REGISTRATION = "registration"
    PURPOSE_PASSWORD_RESET = "password_reset"
    PURPOSE_PIN_RESET = "pin_reset"

    PURPOSE_CHOICES = [
        (PURPOSE_REGISTRATION, "Registration"),
        (PURPOSE_PASSWORD_RESET, "Password reset"),
        (PURPOSE_PIN_RESET, "PIN reset"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otp_verifications",
    )

    channel = models.CharField(
        max_length=10,
        choices=CHANNEL_CHOICES,
    )

    purpose = models.CharField(
        max_length=30,
        choices=PURPOSE_CHOICES,
    )

    code_hash = models.CharField(
        max_length=128,
    )

    expires_at = models.DateTimeField()

    attempts = models.PositiveIntegerField(
        default=0,
    )

    max_attempts = models.PositiveIntegerField(
        default=5,
    )

    is_used = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    verified_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    @staticmethod
    def generate_code():
        """
        Generate a secure six-digit OTP code.
        """
        return f"{secrets.randbelow(1_000_000):06d}"

    def set_code(self, code):
        """
        Store only the SHA-256 hash of the OTP code.
        """
        self.code_hash = hashlib.sha256(
            code.encode("utf-8")
        ).hexdigest()

    def check_code(self, code):
        """
        Compare the submitted code with the stored hash.
        """
        code_hash = hashlib.sha256(
            code.encode("utf-8")
        ).hexdigest()

        return secrets.compare_digest(
            self.code_hash,
            code_hash,
        )

    def is_expired(self):
        """
        Check whether the OTP has expired.
        """
        return timezone.now() >= self.expires_at

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.channel} - "
            f"{self.purpose}"
        )