from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'user_link', 'project', 'task_link', 'created_at')
    list_filter = ('activity_type', 'created_at', 'project', 'user')
    search_fields = ('title', 'description', 'user__username', 'project__name', 'task__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        ('Activity Info', {
            'fields': ('title', 'description', 'activity_type')
        }),
        ('Relations', {
            'fields': ('user', 'project', 'task')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        url = f"/admin/auth/user/{obj.user.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def task_link(self, obj):
        if obj.task:
            url = f"/admin/yourapp/task/{obj.task.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.task.title)
        return '-'
    task_link.short_description = 'Task'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'project', 'task')