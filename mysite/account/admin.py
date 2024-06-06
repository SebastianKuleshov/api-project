from django.contrib import admin
from .models import Account

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'bio', 'location', 'birth_date', 'avatar']

admin.site.register(Account, AccountAdmin)