import logging
import random

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q

from tasks.models import Task, Project
from .models import User, PasswordResetOTP

logger = logging.getLogger(__name__)


# ===================== DECORATOR ===================== #
def anonymous_required(view_func):
    """Prevent logged-in users from accessing auth pages"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# ===================== UTIL ===================== #
def generate_otp():
    return str(random.randint(100000, 999999))


# ===================== EXCEPTION ===================== #
class AccountsException(Exception):
    def __init__(self, message):
        super().__init__(message)


# ===================== VALIDATION ===================== #
def validate_registration(username, email, password, confirm_password, role):
    if not all([username, email, password, confirm_password]):
        raise AccountsException("All required fields are required")

    if len(password) < 8:
        raise AccountsException("Password must be at least 8 characters")

    if password != confirm_password:
        raise AccountsException("Passwords do not match")

    if User.objects.filter(username=username).exists():
        raise AccountsException("Username already exists")

    if User.objects.filter(email=email).exists():
        raise AccountsException("Email already registered")

    if role not in dict(User.ROLE_CHOICES):
        raise AccountsException("Invalid role selected")


# ===================== REGISTER ===================== #
@anonymous_required
def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password1', '').strip()
        confirm_password = request.POST.get('password2', '').strip()
        phone = request.POST.get('phone', '').strip()
        role = request.POST.get('role', '').strip()
        location = request.POST.get('location', '').strip()
        bio = request.POST.get('bio', '').strip()

        try:
            validate_registration(username, email, password, confirm_password, role)

            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    phone=phone,
                    role=role,
                    location=location,
                    bio=bio
                )

                avatar = request.FILES.get('avatar')
                if avatar:
                    user.avatar.save(avatar.name, avatar)

            messages.success(request, "Account created successfully")
            return redirect('login')

        except AccountsException as e:
            messages.error(request, str(e))
            logger.warning(f"Register error: {e}")

        except Exception as e:
            logger.critical(f"Register crash: {e}", exc_info=True)
            messages.error(request, "Something went wrong")

    return render(request, "accounts/register.html")


# ===================== LOGIN ===================== #
@anonymous_required
def login(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            if not email or not password:
                raise AccountsException("Email and password required")

            user_obj = User.objects.filter(email=email).first()
            if not user_obj:
                raise AccountsException("Invalid credentials")

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is None:
                raise AccountsException("Invalid credentials")

            if not user.is_active:
                raise AccountsException("Account inactive")

            auth_login(request, user)
            return redirect('dashboard')

        except AccountsException as e:
            messages.error(request, str(e))
            logger.warning(f"Login error: {e}")

        except Exception as e:
            logger.critical(f"Login crash: {e}", exc_info=True)
            messages.error(request, "Something went wrong")

    return render(request, "accounts/login.html")


# ===================== DASHBOARD ===================== #
@login_required
def dashboard(request):
    try:
        user_projects = Project.objects.filter(
            Q(owner=request.user) | Q(members=request.user)
        ).distinct()

        user_tasks = Task.objects.filter(
            Q(project__in=user_projects) |
            Q(assigned_to=request.user) |
            Q(created_by=request.user)
        ).select_related('project', 'assigned_to', 'created_by')

        stats = {
            'total_projects': user_projects.count(),
            'total_tasks': user_tasks.count(),
            'completed_tasks': user_tasks.filter(is_completed=True).count(),
            'in_progress_tasks': user_tasks.filter(status='in_progress').count(),
            'todo_tasks': user_tasks.filter(status='todo').count(),
        }

        context = {
            'stats': stats,
            'user_projects': user_projects,
            'user_tasks': user_tasks[:12],
            'recent_tasks': user_tasks.order_by('-id')[:5]
        }

        return render(request, "dashboard.html", context)

    except Exception as e:
        logger.critical(f"Dashboard error: {e}", exc_info=True)
        messages.error(request, "Unable to load dashboard")
        return redirect('login')


# ===================== FORGET PASSWORD ===================== #
@anonymous_required
def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        try:
            if not email:
                raise AccountsException("Email required")

            user = User.objects.filter(email=email).first()

            if user:
                otp = generate_otp()
                PasswordResetOTP.objects.filter(user=user).delete()
                PasswordResetOTP.objects.create(user=user, otp=otp)

                send_mail(
                    "OTP for Password Reset",
                    f"Your OTP is {otp} (valid 5 min)",
                    "noreply@taskmanager.com",
                    [email],
                )

            request.session['email'] = email
            messages.success(request, "OTP sent if account exists")
            return redirect("verify_otp")

        except Exception as e:
            logger.critical(f"Forget error: {e}", exc_info=True)
            messages.error(request, "Something went wrong")

    return render(request, "accounts/forget_password.html")


# ===================== VERIFY OTP ===================== #
@anonymous_required
def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        otp = request.POST.get("otp", "").strip()

        try:
            user = User.objects.filter(email=email).first()
            record = PasswordResetOTP.objects.filter(user=user).first()

            if not user or not record:
                raise AccountsException("Invalid request")

            if record.is_expired():
                record.delete()
                raise AccountsException("OTP expired")

            if record.otp != otp:
                raise AccountsException("Invalid OTP")

            request.session['reset_user'] = user.id
            return redirect("reset_password")

        except AccountsException as e:
            messages.error(request, str(e))

    return render(request, "accounts/verify_otp.html")


# ===================== RESET PASSWORD ===================== #
@anonymous_required
def reset_password(request):
    user_id = request.session.get('reset_user')

    if not user_id:
        return redirect("login")

    user = User.objects.filter(id=user_id).first()

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        try:
            if len(password) < 8:
                raise AccountsException("Weak password")

            if password != confirm_password:
                raise AccountsException("Passwords do not match")

            user.password = make_password(password)
            user.save()

            PasswordResetOTP.objects.filter(user=user).delete()
            request.session.flush()

            messages.success(request, "Password reset successful")
            return redirect("login")

        except AccountsException as e:
            messages.error(request, str(e))

    return render(request, "accounts/reset_password.html")


# ===================== LOGOUT ===================== #
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')