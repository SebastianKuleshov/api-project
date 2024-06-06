from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Account
        fields = '__all__'