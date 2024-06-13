from .models import OTP
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.conf import settings

import random

def generate_otp(email=None, phone=None, antifishing_phrase=None):
    kwargs = {"email": email} if email else {"phone": phone}
    otp = OTP.objects.filter(**kwargs).last()

    if otp and otp.is_valid() and otp.used == False:
        return False

    if email:
        otp_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        otp = OTP.objects.create(otp_code=otp_code, **kwargs)

        html_message = render_to_string("user_auth/email.html", {"otp_code": otp_code, "antifishing_phrase": antifishing_phrase})
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            "Your OTP code",
            plain_message,
            settings.EMAIL_HOST_USER,
            [email],

        )

        message.attach_alternative(html_message, "text/html")
        message.send()

    else:
        otp_code = "111111"
        otp = OTP.objects.create(otp_code=otp_code, **kwargs)

    return otp


def verify_otp(otp_code, email=None, phone=None):
    kwargs = {"email": email} if email else {"phone": phone}
    otp = OTP.objects.filter(otp_code=otp_code,**kwargs).last()
    if otp and otp.is_valid():
        otp.used = True
        otp.save()
        return True
    return False
