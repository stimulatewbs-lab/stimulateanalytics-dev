from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

User = get_user_model()

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password'
        )

    return render(
        request,
        'accounts/login.html'
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(
        request,
        'accounts/profile.html',
        {
            'user_obj': request.user
        }
    )


@login_required
def user_list(request):

    users = User.objects.all().order_by('username')

    return render(
        request,
        'accounts/user_list.html',
        {
            'users': users
        }
    )