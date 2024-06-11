from django.contrib.auth import authenticate, login, get_user_model
from rest_framework import serializers
from .models import generate_otp, verify_otp

User = get_user_model()

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    login_confirm = serializers.BooleanField()
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.login_confirm = validated_data.get('login_confirm', instance.login_confirm)
        instance.save()
        return instance

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone'):
            raise serializers.ValidationError("Email or phone is required")
        return super().validate(attrs)

    def create(self, validated_data):
        self.context['request'].session['registration_data'] = validated_data
        if 'email' in validated_data:
            generate_otp(validated_data["email"])
        
        return validated_data


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user and user.is_active:     
            if user.login_confirm:
                generate_otp(user.email)
                self.context['request'].session['registration_data'] = data
                return {"otp_required": True, "user_id": user.id}       
            login(self.context['request'], user)
            return {"user": user}
        raise serializers.ValidationError("Incorrect Credentials")
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
        }


class ConfirmOTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField()

    def create(self, validated_data):
        registration_data = self.context['request'].session.get('registration_data')
        if not registration_data:
            raise serializers.ValidationError("No registration data found")
        if 'email' in registration_data:
            email = registration_data.get('email')
        else:
            email = User.objects.get(username=registration_data.get('username')).email
        if verify_otp(email, validated_data["otp_code"]):
            new_user, created = User.objects.get_or_create(
                username = registration_data.get('username'),
                email = email,
            )
            if created:
                new_user.set_password(registration_data.get('password'))
                new_user.save()
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
