from django.shortcuts import render
from accounts.models import User


def index(request):
    return render(request,"base.html")

def register(request):
    return render(request,"accounts/forget_password.html")

def login(request):
    return render(request,"accounts/login.html")


def forget_passowrd(request):
    return render(request,"accounts/forget_password.html")


def reset_password(request):
    return render(request,"accounts/reset_password.html")

