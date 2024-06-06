from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']
