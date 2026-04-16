from django.shortcuts import render
from .models import Task,Project
from accounts.models import User

from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render
from datetime import datetime
import random

def label_list(request):
    return render(request, 'tasks/label_list.html')


# Project
from django.shortcuts import render, get_object_or_404
from .models import Project

def project_detail(request, id):
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('tasks'),
        pk=id
    )

    tasks = project.tasks.all().order_by('-id')

    total_tasks = tasks.count()
    todo_tasks = tasks.filter(status='todo').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    done_tasks = tasks.filter(status='done').count()
    open_tasks = todo_tasks + in_progress_tasks
    progress_percent = int((done_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    context = {
        'project': project,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
        'open_tasks': open_tasks,
        'progress_percent': progress_percent,
    }
    return render(request, 'projects/project_detail.html', context)

from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import Project, Task

User = get_user_model()

def project_list(request):
    projects = Project.objects.select_related('owner').prefetch_related('tasks').annotate(
        task_count=Count('tasks')
    )

    search = request.GET.get('search')
    owner_id = request.GET.get('owner')
    task_status = request.GET.get('task_status')

    if search:
        projects = projects.filter(name__icontains=search)
    if owner_id:
        projects = projects.filter(owner_id=owner_id)
    if task_status:
        projects = projects.filter(tasks__status=task_status).distinct()

    # PAGINATION (10 projects per page)
    paginator = Paginator(projects, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Stats (total counts, not filtered)
    distinct_owners = Project.objects.values('owner').distinct().count()
    all_tasks = Task.objects.all()
    active_tasks = all_tasks.exclude(status='done').count()
    completed_tasks = all_tasks.filter(status='done').count()
    all_users = User.objects.order_by('username')

    context = {
        'page_obj': page_obj,  # Changed from 'projects'
        'distinct_owners': distinct_owners,
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'all_users': all_users,
        'search': search or '',
        'owner': owner_id or '',
        'task_status': task_status or '',
    }
    return render(request, 'projects/project_list.html', context)
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from .models import Project

User = get_user_model()

def project_create(request):
    all_users = User.objects.order_by("username")
    errors = {}
    values = {
        "name": "",
        "owner": str(request.user.id) if request.user.is_authenticated else "",
        "description": "",
    }

    if request.method == "POST":
        values["name"] = request.POST.get("name", "").strip()
        values["owner"] = request.POST.get("owner", "").strip()
        values["description"] = request.POST.get("description", "").strip()

        if not values["name"]:
            errors["name"] = "Project name is required."

        if not values["owner"]:
            errors["owner"] = "Owner is required."

        owner_obj = None
        if values["owner"]:
            try:
                owner_obj = User.objects.get(id=values["owner"])
            except User.DoesNotExist:
                errors["owner"] = "Selected owner is invalid."

        if not errors:
            project = Project.objects.create(
                name=values["name"],
                owner=owner_obj,
                description=values["description"],
            )
            messages.success(request, f'Project "{project.name}" created successfully.')
            return redirect("project_list")

    context = {
        "all_users": all_users,
        "errors": errors,
        "values": values,
    }
    return render(request, "projects/project_create.html", context)

def project_delete(request,id ):
    project=Project.objects.get(id=id)
    project.delete()
    return redirect('project_list')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()

def project_update(request, id):
    project = get_object_or_404(Project, pk=id)
    all_users = User.objects.order_by('username')

    errors = {}

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        owner_id = request.POST.get('owner', '').strip()
        description = request.POST.get('description', '').strip()

        # Basic validation
        if not name:
            errors['name'] = 'Project name is required.'
        if not owner_id:
            errors['owner'] = 'Owner is required.'

        if not errors:
            try:
                owner = User.objects.get(id=owner_id)
                project.name = name
                project.owner = owner
                project.description = description
                project.save()
                messages.success(request, f"Project “{project.name}” updated successfully.")
                return redirect('project_detail', pk=project.id)
            except User.DoesNotExist:
                errors['owner'] = 'Selected owner does not exist.'

    # On GET or failed POST, keep form data in context
    context = {
        'project': project,
        'all_users': all_users,
        'errors': errors,
    }
    return render(request, 'projects/project_update.html', context)

# Task
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import Http404
from .models import Task

def task_detail(request, id):
    """
    Show a single task with project, assignee, and comments.
    """
    try:
        task = Task.objects \
            .select_related('project', 'project__owner', 'created_by', 'assigned_to') \
            .prefetch_related('comments__user') \
            .get(pk=id)
    except Task.DoesNotExist:
        # Optionally show a 404 page or redirect
        raise Http404("Task not found.")

    # Optional: add some extra context for layout / buttons
    context = {
        'task': task,
    }

    return render(request, 'tasks/task_detail.html', context)
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.select_related('project').all()

    search = request.GET.get('search')
    status = request.GET.get('status')
    priority = request.GET.get('priority')

    if search:
        tasks = tasks.filter(title__icontains=search)
    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)

    # PAGINATION
    paginator = Paginator(tasks, 2)  # 10 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'todo_count': Task.objects.filter(status='todo').count(),
        'in_progress_count': Task.objects.filter(status='in_progress').count(),
        'done_count': Task.objects.filter(status='done').count(),
        'search': search or '',
        'status': status or '',
        'priority': priority or '',
    }
    return render(request, 'tasks/task_list.html', context)


def task_create(request):
    if request.method=="POST":
        task_title=request.POST.get('title','').strip()
        description=request.POST.get('descritption','').strip()
        status=request.POST.get('status','').strip()
        priority=request.POST.get('priority','').strip()
        is_completed=request.POST.get('is_completed','').strip()
        project_id=request.POST.get('project','').strip()
        due_date=request.POST.get('due_date','').strip()
        assigned_to=request.POST.get('assigned_to','').strip()
        Task.objects.create()
    STATUS_CHOICES = ["To Do","In Progress","Review","Done"]
    PRIORITY_CHOICES = ["Low","Medium","High","Urgent"]
    ASSIGN_CHOICES=['Admin','Manger']
    ASSIGN_USERNAME=User.objects.all().values('username')
    print(ASSIGN_USERNAME)
    project=Project.objects.all()
    context={
        'Projects':project,
        'STATUS_CHOICES':STATUS_CHOICES,
        'PRIORITY_CHOICES':PRIORITY_CHOICES,
        'ASSIGN_CHOICES':ASSIGN_CHOICES,
        'ASSIGN_USERNAME':ASSIGN_USERNAME,
        }
    return render(request, 'tasks/task_create.html',context)

def task_delete(request,id):
    task=Task.objects.get(id=id)
    task.delete()

    return redirect('task_list')

def task_update(request,id):
    task=Task.objects.get(id=id)
    # Dummy data for testing
    dummy_data = {
        'task': task,
        'dummy_title': 'Sample Task Title',
        'dummy_description': 'This is a dummy description for testing purposes.',
        'dummy_status': 'in_progress',
        'dummy_priority': 'high',
        'dummy_assigned_to': 'John Doe',
        'dummy_project': 'Sample Project',
    }
    return render(request,"tasks/task_update.html", dummy_data)