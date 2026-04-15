from django.shortcuts import render
from tasks.models import Task



from django.shortcuts import render
from types import SimpleNamespace

from types import SimpleNamespace

def profile(request):
    user = SimpleNamespace(
        id=1,
        username="farhan",
        email="farhan@example.com",
        date_joined="2025-08-12",
        get_full_name="Farhan Ali"
    )

    profile = SimpleNamespace(
        id=1,   # ✅ IMPORTANT
        user=user,
        role="Frontend Developer",
        bio="Focused on building clean interfaces...",
        phone="+91-9876543210",
        open_tasks_count=7,
        project_count=4,
        completed_tasks_count=18,
    )

    return render(request, "users/profile.html", {"profile": profile})

from types import SimpleNamespace

def profile_edit(request, id):
    user = SimpleNamespace(
        first_name="Farhan",
        last_name="Ali",
        email="farhan@example.com"
    )

    profile = SimpleNamespace(
        id=id,
        user=user,
        role="Frontend Developer",
        bio="Focused on building clean interfaces...",
        phone="+91-9876543210"
    )

    return render(request, "users/profile_edit.html", {'profile': profile})  


from django.shortcuts import render

def users_list(request):
    users = [
        {
            "username": "john",
            "full_name": "John Doe",
            "email": "john@example.com",
            "profile": {"role": "Admin"},
        },
        {
            "username": "sarah",
            "full_name": "Sarah Khan",
            "email": "sarah@example.com",
            "profile": {"role": "Manager"},
        },
        {
            "username": "alex",
            "full_name": "Alex Roy",
            "email": "alex@example.com",
            "profile": {"role": "Developer"},
        },
        {
            "username": "tina",
            "full_name": "Tina Mehta",
            "email": "tina@example.com",
            "profile": {"role": "Designer"},
        },
        {
            "username": "mike",
            "full_name": "Mike Chang",
            "email": "mike@example.com",
            "profile": {"role": "Member"},
        },
    ]
    return render(request, "users/users_list.html", {
        "users": users
    })

