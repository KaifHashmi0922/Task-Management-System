# activity.py (add this to your existing models.py)
from django.conf import settings
from django.db import models
from django.utils import timezone
from accounts.models import User
from tasks.models import Project,Task,Comment,Label,Attachment

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('update', 'Update'),
        ('create', 'Create'),
        ('delete', 'Delete'),
        ('assign', 'Assign'),
        ('complete', 'Complete'),
        ('comment', 'Comment'),
        ('label', 'Label'),
        ('priority', 'Priority'),
        ('status', 'Status'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='activities',
        null=True, 
        blank=True
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='activities'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.activity_type}"