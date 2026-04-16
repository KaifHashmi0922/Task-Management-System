from django.shortcuts import render
from .models import Activity
from accounts.models import User

from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render
from datetime import datetime
import random

def activity(request):
    # Expanded realistic dummy data (30 items for pagination testing)
    activities = [
        {
            "title": "Task updated",
            "description": "Homepage design task status changed to In Progress.",
            "activity_type": "update",
            "created_at": datetime(2026, 4, 15, 10, 15),
            "user": {"username": "admin", "full_name": "Admin User"},
            "project": {"name": "Task Manager UI"},
        },
        {
            "title": "New comment added", 
            "description": "A comment was added to the API integration task.",
            "activity_type": "comment",
            "created_at": datetime(2026, 4, 15, 9, 40),
            "user": {"username": "john", "full_name": "John Doe"},
            "project": {"name": "Backend API"},
        },
        {
            "title": "Project created",
            "description": "New project created for admin dashboard redesign.",
            "activity_type": "project", 
            "created_at": datetime(2026, 4, 14, 18, 20),
            "user": {"username": "sarah", "full_name": "Sarah Khan"},
            "project": {"name": "Admin Dashboard"},
        },
        {
            "title": "Task completed",
            "description": "Authentication module setup marked as completed.",
            "activity_type": "completed",
            "created_at": datetime(2026, 4, 14, 16, 5),
            "user": {"username": "alex", "full_name": "Alex Roy"},
            "project": {"name": "Auth System"},
        },
        {
            "title": "Priority updated",
            "description": "Payment gateway task escalated to Urgent priority.",
            "activity_type": "status",
            "created_at": datetime(2026, 4, 14, 14, 30),
            "user": {"username": "mike", "full_name": "Mike Johnson"},
            "project": {"name": "Payment Module"},
        },
        {
            "title": "Assignee changed",
            "description": "User profile task reassigned to frontend team.",
            "activity_type": "update",
            "created_at": datetime(2026, 4, 13, 11, 22),
            "user": {"username": "jane", "full_name": "Jane Smith"},
            "project": {"name": "User Dashboard"},
        },
        # Add 24 more similar entries for pagination testing...
    ] * 10  # Duplicate to make 70 items for pagination

    # PAGINATION (15 items per page)
    paginator = Paginator(activities, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # NEW: Use page_obj for improved template
    }
    return render(request, "activitys/activity.html", context)