from django.contrib.auth import authenticate, login, get_user_model
from pkg_resources import require
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .utils import generate_otp, verify_otp

User = get_user_model()

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    login_confirm = serializers.BooleanField()
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.login_confirm = validated_data.get('login_confirm', instance.login_confirm)
        instance.save()
        return instance

class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    phone = serializers.CharField(max_length=20, required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    antifishing_phrase = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError("Email or phone is required")
        return super().validate(data)

    def create(self, validated_data):
        self.context['request'].session['registration_data'] = validated_data
        email = validated_data.get('email', None)
        phone = validated_data.get('phone', None)
        antifishing_phrase = validated_data.get('antifishing_phrase', None)
        generate_otp(email=email, phone=phone, antifishing_phrase=antifishing_phrase)    
        
        return validated_data


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=20, required=False)
    password = serializers.CharField()

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError("Email or phone is required")
        kwargs = {'email': data.get('email')} if data.get('email') else {'phone': data.get('phone')}
        user = authenticate(password=data["password"], **kwargs)
        if user and user.is_active:     
            if user.login_confirm:
                generate_otp(user.email)
                self.context['request'].session['registration_data'] = data
                self.context['request'].session['registration_data']['old_user'] = 'True'
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
        email = registration_data.get('email', None)
        phone = registration_data.get('phone', None)
        old_user = registration_data.get('old_user', None)

        if verify_otp(validated_data["otp_code"], email=email, phone=phone):
            new_user, created = User.objects.get_or_create(
                email = email,
                phone = phone,
            )
            if created:
                new_user.set_password(registration_data.get('password'))
                new_user.save()
            login(self.context['request'], new_user)
            try:
                del self.context['request'].session['registration_data']
            except KeyError:
                print("No registration data found")
            return new_user
        raise serializers.ValidationError("Invalid OTP code")

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "phone": instance.phone,
        }
