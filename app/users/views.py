from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm


def loginuser(request):
    """Login form for user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    contex = {}
    return render(request, 'users/login.html', contex)


def logoutuser(request):
    """User logged out from dashboard"""
    logout(request)
    return redirect('login')


def registeruser(request):
    """User registration form to create user """
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+user)
            return redirect('login')

    contex = {'form': form}
    return render(request, 'users/register.html', contex)


@login_required(login_url='login')
def home(request):
    """Dashboard views after successfull login"""
    return render(request, 'users/dashboard.html')
