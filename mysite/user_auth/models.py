from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from datetime import timedelta

# Create your models here.


class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    login_confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.email if self.email else self.phone

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_email_or_phone",
                check=(
                    models.Q(email__isnull=True, phone__isnull=False)
                    | models.Q(email__isnull=False, phone__isnull=True)
                    | models.Q(email__isnull=False, phone__isnull=False)
                ),
            )
        ]


class OTP(models.Model):
    otp_code = models.CharField(max_length=6)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at < timedelta(minutes=5)
