from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from game.models import Level, UserProgress, UserStats
from django.contrib.auth.models import User
import json


def signup(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('game:play')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user stats
            UserStats.objects.create(user=user)
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome to CSS Bunny, {user.username}!')
            return redirect('game:dashboard') # Redirect to dashboard to see new stats
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Custom login view that accepts username or email"""
    if request.user.is_authenticated:
        return redirect('game:play')
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to find user by username or email
        user = None
        if '@' in username_or_email:
            # It's an email
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            # It's a username
            user = authenticate(request, username=username_or_email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('game:play')
        else:
            messages.error(request, 'Invalid username/email or password.')
    
    return render(request, 'accounts/login.html')
def logout_view(request):
    """Custom logout view that handles both GET and POST"""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')
