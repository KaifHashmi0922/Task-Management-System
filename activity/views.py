from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse
from .models import Activity
from tasks.models import Project, Task


# ✅ CREATE ACTIVITY
@login_required
def create_activity(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        activity_type = request.POST.get('activity_type')
        project_id = request.POST.get('project_id')
        task_id = request.POST.get('task_id')

        project = get_object_or_404(Project, id=project_id)
        task = Task.objects.filter(id=task_id).first()  # optional

        Activity.objects.create(
            title=title,
            description=description,
            activity_type=activity_type,
            project=project,
            task=task,
            user=request.user,
            created_at=timezone.now()
        )

        return redirect('activity_list')

    context = {
        'projects': Project.objects.all(),
        'tasks': Task.objects.all()
    }
    return render(request, 'activity/create.html', context)


# ✅ ACTIVITY LIST (DB + PAGINATION)
# @login_required
# def activity_list(request):
#     activities = Activity.objects.select_related(
#         'user', 'project', 'task'
#     ).all()

#     paginator = Paginator(activities, 10)  # 10 per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'activity/list.html', {
#         'page_obj': page_obj
#     })
from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime


def activity_list(request):

    activities = [
        {
            "id":1,
            "title": "Task Updated",
            "description": "Homepage design moved to In Progress.",
            "activity_type": "update",
            "created_at": datetime(2026, 4, 15, 10, 15),
            "user": {"username": "admin", "full_name": "Admin User"},
            "project": {"name": "Task Manager UI"},
        },
        {   "id":2,
            "title": "Comment Added",
            "description": "New comment added on API task.",
            "activity_type": "comment",
            "created_at": datetime(2026, 4, 15, 9, 40),
            "user": {"username": "john", "full_name": "John Doe"},
            "project": {"name": "Backend API"},
        },
        {
             "id":3,
            "title": "Project Created",
            "description": "New admin dashboard project created.",
            "activity_type": "create",
            "created_at": datetime(2026, 4, 14, 18, 20),
            "user": {"username": "sarah", "full_name": "Sarah Khan"},
            "project": {"name": "Admin Dashboard"},
        },
        {
             "id":4,
            "title": "Task Completed",
            "description": "Authentication setup marked complete.",
            "activity_type": "complete",
            "created_at": datetime(2026, 4, 14, 16, 5),
            "user": {"username": "alex", "full_name": "Alex Roy"},
            "project": {"name": "Auth System"},
        },
        {
             "id":5,
            "title": "Priority Changed",
            "description": "Payment task set to High priority.",
            "activity_type": "priority",
            "created_at": datetime(2026, 4, 14, 14, 30),
            "user": {"username": "mike", "full_name": "Mike Johnson"},
            "project": {"name": "Payment Module"},
        },
        {
             "id":6,
            "title": "Task Assigned",
            "description": "Profile task assigned to frontend team.",
            "activity_type": "assign",
            "created_at": datetime(2026, 4, 13, 11, 22),
            "user": {"username": "jane", "full_name": "Jane Smith"},
            "project": {"name": "User Dashboard"},
        },
        {
             "id":7,
            "title": "Status Changed",
            "description": "Bug fixing moved to Testing phase.",
            "activity_type": "status",
            "created_at": datetime(2026, 4, 13, 10, 10),
            "user": {"username": "rohit", "full_name": "Rohit Sharma"},
            "project": {"name": "Bug Tracker"},
        },
        {
             "id":8,
            "title": "Label Added",
            "description": "UI task tagged as 'Frontend'.",
            "activity_type": "label",
            "created_at": datetime(2026, 4, 12, 15, 45),
            "user": {"username": "aman", "full_name": "Aman Verma"},
            "project": {"name": "UI Revamp"},
        },
    ] * 8  # total ~64 records

    # ✅ PAGINATION
    paginator = Paginator(activities, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "activitys/activity.html", {
        'page_obj': page_obj
    })

# ✅ ACTIVITY DETAIL
from django.shortcuts import render
from datetime import datetime


def activity_detail(request, id):

    activities = [
        {
            "id": 1,
            "title": "Task Updated",
            "description": "Homepage design moved to In Progress.",
            "activity_type": "update",
            "created_at": datetime(2026, 4, 15, 10, 15),
            "user": {"username": "admin"},
            "project": {"name": "Task Manager UI"},
        },
        {
            "id": 2,
            "title": "Comment Added",
            "description": "New comment added on API task.",
            "activity_type": "comment",
            "created_at": datetime(2026, 4, 15, 9, 40),
            "user": {"username": "john"},
            "project": {"name": "Backend API"},
        },
        {
            "id": 3,
            "title": "Project Created",
            "description": "New admin dashboard project created.",
            "activity_type": "create",
            "created_at": datetime(2026, 4, 14, 18, 20),
            "user": {"username": "sarah"},
            "project": {"name": "Admin Dashboard"},
        },
    ]

    # 🔥 Find activity by id
    activity = next((a for a in activities if a["id"] == id), None)

    if not activity:
        return render(request, "activitys/detail.html", {
            "error": "Activity not found"
        })

    return render(request, "activitys/activity_detail.html", {
        "activity": activity
    })


# ✅ UPDATE ACTIVITY
# @login_required
# def update_activity(request, id):
#     activity = get_object_or_404(Activity, id=id)

#     if request.method == "POST":
#         activity.title = request.POST.get('title')
#         activity.description = request.POST.get('description')
#         activity.activity_type = request.POST.get('activity_type')

#         project_id = request.POST.get('project_id')
#         task_id = request.POST.get('task_id')

#         activity.project = get_object_or_404(Project, id=project_id)
#         activity.task = Task.objects.filter(id=task_id).first()

#         activity.save()

#         return redirect('activity_detail', id=activity.id)

#     context = {
#         'activity': activity,
#         'projects': Project.objects.all(),
#         'tasks': Task.objects.all()
#     }
#     return render(request, 'activity/activity_edit.html', context)


# ✅ DELETE ACTIVITY
@login_required
def delete_activity(request, id):
    activity = get_object_or_404(Activity, id=id)

    if request.method == "POST":
        activity.delete()
        return redirect('activity_list')

    return render(request, 'activity/delete.html', {
        'activity': activity
    })
    
    
    
    
    from django.shortcuts import render, redirect
from datetime import datetime

# 🔥 shared dummy data function
def get_dummy_activities():
    return [
        {
            "id": 1,
            "title": "Task Updated",
            "description": "Homepage design moved to In Progress.",
            "activity_type": "update",
            "created_at": datetime(2026, 4, 15, 10, 15),
            "user": {"username": "admin"},
            "project": {"name": "Task Manager UI"},
        },
        {
            "id": 2,
            "title": "Comment Added",
            "description": "New comment added on API task.",
            "activity_type": "comment",
            "created_at": datetime(2026, 4, 15, 9, 40),
            "user": {"username": "john"},
            "project": {"name": "Backend API"},
        },
    ]


def update_activity(request, id):
    activities = get_dummy_activities()

    # 🔥 find activity
    activity = next((a for a in activities if a["id"] == id), None)

    if not activity:
        return render(request, "activity/activity_edit.html", {
            "error": "Activity not found"
        })

    if request.method == "POST":
        # 🔥 update dummy data (temporary)
        activity["title"] = request.POST.get("title")
        activity["description"] = request.POST.get("description")
        activity["activity_type"] = request.POST.get("activity_type")

        # ⚠️ no DB save here

        return redirect("activity_detail", id=id)

    return render(request, "activitys/activity_edit.html", {
        "activity": activity,
        "projects": [],   # dummy empty
        "tasks": []       # dummy empty
    })
    
    
    
def create_activity(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        activity_type = request.POST.get('activity_type')
        project_id = request.POST.get('project_id')
        task_id = request.POST.get('task_id')

        project = Project.objects.get(id=project_id)
        task = Task.objects.filter(id=task_id).first()

        Activity.objects.create(
            title=title,
            description=description,
            activity_type=activity_type,
            project=project,
            task=task,
            user=request.user
        )

        return redirect('activity_list')

    return render(request, 'activitys/activity_create.html', {
        'projects': Project.objects.all(),
        'tasks': Task.objects.all(),
        'activity': Activity  # for ACTIVITY_TYPES
    })
    
    
    
def task_edit(request,id):
    if request.method=="POST":
        tasks=Task.objects.all()
        print(len(task))
    return HttpResponse("its working")