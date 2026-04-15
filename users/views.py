from django.shortcuts import render
from tasks.models import Task



from django.shortcuts import render
from types import SimpleNamespace

def profile(request):
    user = SimpleNamespace(
        username="farhan",
        email="farhan@example.com",
        date_joined="2025-08-12",
        get_full_name="Farhan Ali"
    )

    profile = SimpleNamespace(
        user=user,
        role="Frontend Developer",
        bio="Focused on building clean interfaces, improving UX, and collaborating across design and backend teams.",
        open_tasks_count=7,
        project_count=4,
        completed_tasks_count=18,
    )

    return render(request, "users/profile.html", {"profile": profile})

def profile_edit(request):
    profile={

    "user": {
        "first_name": "Aman",
        "last_name": "Sharma",
        "email": "aman.sharma@example.com"
    },
    "bio": "Enthusiastic developer who enjoys building web applications.",
    "role": "Frontend Developer",
    "phone": "+91-9876543210"
        }    
    return render(request,"users/profile_edit.html",{'proflie':profile})


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

