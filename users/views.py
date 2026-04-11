from django.shortcuts import render
from tasks.models import Task



def profile(request):
    return render(request,"tasks/dashboard.html")

def profile_edit(request):
    return render(request,"tasks/label_list.html")


def user_list(request):
    return render(request,"tasks/task_register.html")

