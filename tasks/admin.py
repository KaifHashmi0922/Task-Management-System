from django.contrib import admin
from .models import Project, Label, Task, Comment, Attachment

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("title", "assigned_to", "status", "priority", "due_date", "is_completed")
    show_change_link = True

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("user", "body", "created_at")
    can_delete = False

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    readonly_fields = ("uploaded_at",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_archived", "start_date", "due_date", "created_at")
    list_filter = ("is_archived", "start_date", "due_date", "created_at")
    search_fields = ("name", "description", "owner__username", "members__username")
    ordering = ("-created_at",)
    filter_horizontal = ("members",)
    inlines = [TaskInline]
    readonly_fields = ("created_at",)

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "color")
    list_filter = ("project", "color")
    search_fields = ("name", "project__name")
    ordering = ("name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "assigned_to", "status", "priority", "due_date", "is_completed", "updated_at")
    list_filter = ("status", "priority", "is_completed", "due_date", "project")
    search_fields = ("title", "description", "project__name", "assigned_to__username", "created_by__username")
    ordering = ("-updated_at",)
    filter_horizontal = ("labels",)
    inlines = [CommentInline, AttachmentInline]
    readonly_fields = ("created_at", "updated_at")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("task__title", "user__username", "body")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("task", "file", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("task__title",)
    ordering = ("-uploaded_at",)
    readonly_fields = ("uploaded_at",)