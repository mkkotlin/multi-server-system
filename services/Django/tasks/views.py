from rest_framework import viewsets
from tasks.models import TaskModel
from tasks.serializers import TaskSerializer
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied



# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return TaskModel.objects.select_related("project", "assigned_to").all()
        return TaskModel.objects.select_related("project", "assigned_to").filter(project__owner=user)

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        assigned_to = serializer.validated_data.get("assigned_to")
        user = self.request.user

        if user.role != "ADMIN" and project.owner_id != user.id:
            raise PermissionDenied("You can only create tasks in your own projects.")

        if user.role != "ADMIN" and assigned_to is not None:
            if assigned_to.id != user.id:
                raise PermissionDenied("You can only assign tasks to yourself.")

        serializer.save()

    def perform_update(self, serializer):
        task = serializer.save()
        if task.status == TaskModel.Status.COMPLETED:
            if task.completed_at is None:
                task.completed_at = timezone.now()
                task.save(update_fields=["completed_at"])
        elif task.completed_at is not None:
            task.completed_at = None
            task.save(update_fields=["completed_at"])