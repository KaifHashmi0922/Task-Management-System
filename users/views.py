from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from tasks.models import Task, Project

User = get_user_model()


# ================= PROFILE ================= #
@login_required
def profile(request):
    user = request.user

    # 🔥 REAL COUNTS
    open_tasks = Task.objects.filter(assigned_to=user, is_completed=False).count()
    completed_tasks = Task.objects.filter(assigned_to=user, is_completed=True).count()
    projects = Project.objects.filter(members=user).count()

    context = {
        "profile": {
            "user": user,
            "role": getattr(user, "role", "Member"),
            "bio": getattr(user, "bio", ""),
            "open_tasks_count": open_tasks,
            "project_count": projects,
            "completed_tasks_count": completed_tasks,
        }
    }

    return render(request, "users/profile.html", context)


@login_required
def profile_edit(request, id):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")
        user.phone = request.POST.get("phone", "")
        user.bio = request.POST.get("bio", "")
        user.save()
        return redirect('profile')
    context = {
        "profile": {
            "user": user,
            "id":getattr(user, "id", ""),
            "email":getattr(user, "email", ""),
            "role": getattr(user, "role", ""),
            "bio": getattr(user, "bio", ""),
            "phone": getattr(user, "phone", ""),
        }
    }

    return render(request, "users/profile_edit.html", context)


from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone  # 👈 add this line

User = get_user_model()


@login_required
def users_list(request):
    search = request.GET.get("search", "").strip()
    role = request.GET.get("role", "").strip()
    task_status = request.GET.get("task_status", "").strip()

    users = User.objects.select_related("profile").order_by("last_name", "first_name")

    if search:
        users = users.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )

    if role:
        users = users.filter(profile__role=role)

    paginator = Paginator(users, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    admin_count = users.filter(profile__role="Admin").count()
    # Use timezone.now() now that it’s imported
    active_users_count = users.filter(last_login__date=timezone.now().date()).count()

    return render(
        request,
        "users/users_list.html",
        {
            "page_obj": page_obj,
            "search": search,
            "role": role,
            "task_status": task_status,
            "admin_count": admin_count,
            "active_users_count": active_users_count,
            "is_paginated": page_obj.has_other_pages(),
        },
    )