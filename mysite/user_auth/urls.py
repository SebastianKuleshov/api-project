from django.urls import path
from . import views

app_name = 'user_auth'

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('confirm/', views.confirm_page, name='confirm'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
]
