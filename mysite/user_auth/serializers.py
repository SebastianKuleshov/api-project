from django.contrib.auth import authenticate, login
from rest_framework import serializers
from .models import generate_otp, verify_otp
from django.contrib.auth.models import User


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        self.context['request'].session['registration_data'] = validated_data
        generate_otp(validated_data["email"])
        return validated_data


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user and user.is_active:            
            login(self.context['request'], user)
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class ConfirmOTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField()

    def create(self, validated_data):
        registration_data = self.context['request'].session.get('registration_data')
        if not registration_data:
            raise serializers.ValidationError("No registration data found")
        email = registration_data.get('email')
        if verify_otp(email, validated_data["otp_code"]):
            new_user = User.objects.create_user(
                username = registration_data.get('username'),
                email = email,
                password = registration_data.get('password')
            )
            login(self.context['request'], new_user)
            del self.context['request'].session['registration_data']
            return new_user
        raise serializers.ValidationError("Invalid OTP code")

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
        }
