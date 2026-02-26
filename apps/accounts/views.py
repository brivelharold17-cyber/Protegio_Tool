from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods


# ============ AUTHENTICATION VIEWS ============

@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', 'dashboard:dashboard')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')


@require_http_methods(["GET", "POST"])
def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('accounts:signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('dashboard:dashboard')
    
    return render(request, 'accounts/signup.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('accounts:login')


# ============ USER PROFILE VIEWS ============

@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def activity_log_view(request):
    """User activity log view"""
    return render(request, 'accounts/activity.html')


@login_required
def scan_history_view(request):
    """User scan history view"""
    return render(request, 'accounts/scans.html')


# ============ ADMIN VIEWS ============

@login_required
def admin_users_view(request):
    """Admin users management view"""
    if not request.user.is_staff:
        return redirect('dashboard:dashboard')
    
    users = User.objects.all()
    return render(request, 'accounts/admin_users.html', {'users': users})


@login_required
def admin_audit_log_view(request):
    """Admin audit log view"""
    if not request.user.is_staff:
        return redirect('dashboard:dashboard')
    
    return render(request, 'accounts/admin_audit.html')


# ============ API VIEWS ============

@login_required
def get_audit_stats_api(request):
    """Get audit statistics (API endpoint)"""
    from django.http import JsonResponse
    
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
    }
    
    return JsonResponse(stats)
