from django.db import models
import uuid
from django.conf import settings

# Create your models here.

class TaskModel(models.Model):
    class Status(models.TextChoices):
        TO_DO = "TO_DO", "To_Do"
        IN_PROGRESS = "IN_PROGRESS", "In_Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    project = models.ForeignKey("projects.ProjectModel", on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    status = models.CharField(max_length=20, default=Status.TO_DO, choices=Status.choices)
    priority = models.CharField(max_length=20, default=Priority.MEDIUM, choices=Priority.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title