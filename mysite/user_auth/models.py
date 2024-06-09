from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from datetime import timedelta
import random

# Create your models here.

class OTP(models.Model):
    otp_code = models.CharField(max_length=6)
    email = models.EmailField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def is_valid(self):
        return timezone.now() - self.created_at < timedelta(minutes=5)
    

def generate_otp(email):
    otp = OTP.objects.filter(email=email).last()
    if otp and otp.is_valid() and otp.used == False:
        return False

    otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    otp = OTP.objects.create(otp_code=otp_code, email=email)
    send_mail(
        'Your OTP code',
        f'Your OTP code is {otp_code}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    
    return otp

def verify_otp(email, otp_code):
    otp = OTP.objects.filter(email=email, otp_code=otp_code).last()
    if otp and otp.is_valid():
        otp.used = True
        otp.save()
        return True
    return False