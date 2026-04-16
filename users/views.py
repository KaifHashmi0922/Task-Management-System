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


@login_required
def users_list(request):
    users = User.objects.all()

    return render(request, "users/users_list.html", {
        "users": users
    })