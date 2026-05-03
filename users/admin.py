from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "location", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("user__username", "user__email", "phone", "location")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)