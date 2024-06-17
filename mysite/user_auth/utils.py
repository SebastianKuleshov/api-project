from .models import OTP
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.conf import settings

import random
import string


def send_email_message(email=None, antifishing_phrase=None, otp_method="code", url=None, otp_code=None):
    if otp_method == "code":
        subject = "Your OTP code"
        html_message = render_to_string(
            "user_auth/email.html",
            {"otp_code": otp_code, "antifishing_phrase": antifishing_phrase, "otp_method": otp_method},
        )
    else:
        subject = "Your OTP link"
        link = f"{url}/{otp_code}"
        html_message = render_to_string(
            "user_auth/email.html",
            {"otp_code": link, "antifishing_phrase": antifishing_phrase, "otp_method": otp_method},
        )

    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [email],
    )

    message.attach_alternative(html_message, "text/html")
    message.send()


def send_phone_message(phone=None, antifishing_phrase=None, otp_method="code", url=None, otp_code=None):
    pass


def generate_otp(email=None, phone=None, antifishing_phrase=None, otp_method="code", url=None, resend=False):
    kwargs = {"email": email} if email else {"phone": phone}
    otp = OTP.objects.filter(**kwargs).last()

    if otp and otp.is_valid() and otp.used == False:
        if resend:
            otp_code = otp.otp_code
            if len(otp_code) == 6:
                otp_method = "code"
            else:
                otp_method = "link"
            if email:
                send_email_message(email, antifishing_phrase, otp_method, url, otp_code)
            else:
                send_phone_message(phone, antifishing_phrase, otp_method, url, otp_code)
        else:
            return False
    else:
        if email:
            if otp_method == "code":
                otp_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
                otp = OTP.objects.create(otp_code=otp_code, **kwargs)
            else:
                otp_code = "".join(random.choices(string.ascii_letters + string.digits, k=20))
                otp = OTP.objects.create(otp_code=otp_code, **kwargs)
            send_email_message(email, antifishing_phrase, otp_method, url, otp_code)
        else:
            if otp_method == "code":
                otp_code = "111111"
                otp = OTP.objects.create(otp_code=otp_code, **kwargs)
            else:
                otp_code = "1" * 20
                otp = OTP.objects.create(otp_code=otp_code, **kwargs)
                otp_code = f"{url}/{otp_code}"
            send_phone_message(phone, antifishing_phrase, otp_method, url, otp_code)


def verify_otp(otp_code, email=None, phone=None):
    kwargs = {"email": email} if email else {"phone": phone}
    otp = OTP.objects.filter(otp_code=otp_code, **kwargs).last()
    if otp and otp.is_valid():
        otp.used = True
        otp.save()
        return True
    return False
