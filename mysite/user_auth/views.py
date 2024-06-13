from django.contrib.auth import login, authenticate, logout, get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterUserSerializer, LoginUserSerializer, ConfirmOTPSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from post.permissions import IsOwnerOrAdmin

# Create your views here.


class UserAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "login_confirm": user.login_confirm,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=UserSerializer,
    )
    def patch(self, request):
        serializer = self.serializer_class(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    serializer_class = RegisterUserSerializer

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=RegisterUserSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    serializer_class = LoginUserSerializer

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LoginUserSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            validated_data = serializer.validated_data
            if validated_data.get("otp_required"):
                return Response(
                    {"message": "OTP code sent", "user_id": validated_data["user_id"]}, status=status.HTTP_200_OK
                )
            user = validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": serializer.to_representation(user),
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmOTPAPIView(APIView):
    serializer_class = ConfirmOTPSerializer

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ConfirmOTPSerializer,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {"user": serializer.to_representation(user), "refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
        )


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
