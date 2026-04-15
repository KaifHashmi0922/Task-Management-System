from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.db import IntegrityError
from tasks.models import Task,Attachment,models,Comment,Label,Project



# ---------------- REGISTER ---------------- #
def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect('register')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        try:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Something went wrong")
            return redirect('register')

    return render(request, "accounts/register.html", {'logged_in': False})


# ---------------- LOGIN ---------------- #
def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "All fields are required")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, "accounts/login.html")


# ---------------- DASHBOARD (PROTECTED) ---------------- #
# @login_required
def dashboard(request):
    task=Task.objects.all()
    commnets=Comment.objects.all()
    projects=Project.objects.all()
    recent_task = Task.objects.order_by('-id')[:3]
    
    
    
    stats={'total':50,'completed':10,'pending':2,'overdue':10}
   
    return render(request, "dashboard.html",{'stats':stats,'task':task,'comments':commnets,'projects':projects,'recent_tasks':recent_task})


# ---------------- FORGOT PASSWORD ---------------- #
def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        if not email:
            messages.error(request, "Email is required")
            return redirect("forget_password")

        user = User.objects.filter(email=email).first()

       
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                reverse("reset_password", kwargs={"uidb64": uid, "token": token})
            )

            send_mail(
                "Password Reset",
                f"Click to reset:\n{reset_link}",
                "your_email@gmail.com",
                [email],
            )

        messages.success(request, "If account exists, reset link sent")
        return redirect("login")

    return render(request, "accounts/forget_password.html")


# ---------------- RESET PASSWORD ---------------- #
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if not user or not default_token_generator.check_token(user, token):
        return render(request, "accounts/error.html")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if len(password) < 6:
            return render(request, "accounts/reset.html", {"error": "Weak password"})

        if password != confirm_password:
            return render(request, "accounts/reset.html", {"error": "Passwords do not match"})

        user.password = make_password(password)
        user.save()

        messages.success(request, "Password updated successfully")
        return redirect("login")

    return render(request, "accounts/reset.html")