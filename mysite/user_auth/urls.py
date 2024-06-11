from django.urls import path
from . import views

app_name = 'user_auth'

urlpatterns = [
    path('user/', views.UserAPIView.as_view(), name='user'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('confirm/', views.ConfirmOTPAPIView.as_view(), name='confirm'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),      
]