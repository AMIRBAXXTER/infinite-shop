from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
from .models import User


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(phone=phone, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('IndexApp:index')

    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(phone=cd['phone'], password=cd['password'], first_name=cd['first_name'], last_name=cd['last_name'])
            user = authenticate(phone=cd['phone'], password=cd['password'])
            login(request, user)
            return redirect('IndexApp:index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})