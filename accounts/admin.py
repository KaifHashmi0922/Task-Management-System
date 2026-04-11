from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    list_filter = ("role", "is_staff", "is_active", "is_superuser")
    ordering = ("username",)
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role", "phone", "avatar", "location", "bio")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("role", "phone", "avatar", "location", "bio")}),
    )