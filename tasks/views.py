from django.shortcuts import render

# Activity
def activity(request):
    return render(request, 'tasks/activity.html')


# Dashboard
def dashboard(request):
    return render(request, 'tasks/dashboard.html')


# Labels
def label_list(request):
    return render(request, 'tasks/label_list.html')


# Project
def project_detail(request):
    return render(request, 'tasks/project_detail.html')

def project_list(request):
    return render(request, 'tasks/project_list.html')

def project_register(request):
    return render(request, 'tasks/project_register.html')

def project_delete(request):
    return render(request, 'tasks/project_delete.html')


# Task
def task_detail(request):
    return render(request, 'tasks/task_detail.html')

def task_list(request):
    return render(request, 'tasks/task_list.html')

def task_create(request):
    return render(request, 'tasks/task_register.html')

def task_delete(request):
    return render(request, 'tasks/task_delete.html')