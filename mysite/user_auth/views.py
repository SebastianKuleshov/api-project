from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserRegisterForm, UserLoginForm, ConfirmForm
from rest_framework.permissions import IsAuthenticated
from .models import generate_otp, verify_otp
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, LoginUserSerializer, ConfirmOTPSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class RegisterAPIView(APIView):
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(
        request_body=RegisterUserSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmOTPAPIView(APIView):
    serializer_class = ConfirmOTPSerializer

    @swagger_auto_schema(
        request_body=ConfirmOTPSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.to_representation(user),
            "refresh": str(refresh),
            "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginUserSerializer

    @swagger_auto_schema(
        request_body=LoginUserSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
