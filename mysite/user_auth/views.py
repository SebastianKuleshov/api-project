from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserRegisterForm, UserLoginForm, ConfirmForm
from .models import generate_otp, verify_otp

# Create your views here.

def register_page(request):
    if request.user.is_authenticated:
        return redirect("account:index")
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            if generate_otp(form.cleaned_data['email']):
                request.session['registration_data'] = form.cleaned_data
            # login(request, form.instance)
            return redirect("user_auth:confirm")         
        

    return render(request, 'user_auth/register.html', {'form': form})

def confirm_page(request):
    if request.user.is_authenticated:
        return redirect("account:index")
    form = ConfirmForm()
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            registration_data = request.session.get('registration_data')
            if registration_data:
                email = registration_data['email']
                if verify_otp(email, otp_code):                    
                    User = get_user_model()
                    new_user = User.objects.create_user(
                        username=registration_data['username'],
                        email=registration_data['email'],
                        password=registration_data['password1']
                    )
                    login(request, new_user)
                    del request.session['registration_data']
                    return redirect("account:index")
        
    return render(request, 'user_auth/confirm.html', context={'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("account:index")
    form = UserLoginForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        context['form'] = form
        context['error'] = 'Invalid username or password'
        if user is not None:
            login(request, user)
            return redirect("account:index")
            
    return render(request, 'user_auth/login.html', context=context)

def logout_page(request):
    logout(request)
    return redirect("account:index") 