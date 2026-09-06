from rest_framework import serializers
from tasks.models import TaskModel
from projects.models import ProjectModel
from users.models import User


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset = ProjectModel.objects.all())

    assigned_to = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_active=True).all(), required=False, allow_null=True)

    class Meta:
        model = TaskModel
        fields = ["id", "project", "title", "assigned_to", "status", "priority", "created_at", "updated_at", "completed_at"]
        read_only_fields = ["id", "created_at", "updated_at", "completed_at"]