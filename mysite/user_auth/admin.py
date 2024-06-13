from django.contrib import admin
from .models import CustomUser, OTP

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'login_confirm']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)