from rest_framework import viewsets
from tasks.models import TaskModel
from tasks.serializers import TaskSerializer
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from core.event_service import publish_event



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

        task = serializer.save()
        publish_event(event_type="TASK_CREATED", entity_type="TASK", entity_id=task.id, payload={
            "title": task.title,
            "project_id": str(task.project_id),
            "assigned_to": (
                str(task.assigned_to_id) if task.assigned_to_id else None
            ),
            "priority": task.priority,
            "created_by": str(user.id)
        })

    def perform_update(self, serializer):
        task = self.get_object()
        old_status = task.status

        task = serializer.save()

        if task.status == TaskModel.Status.COMPLETED:

            if task.completed_at is None:
                task.completed_at = timezone.now()
                task.save(update_fields=["completed_at"])

            # Publish only when the task actually becomes completed
            if old_status != TaskModel.Status.COMPLETED:
                publish_event(
                    event_type="TASK_COMPLETED",
                    entity_type="TASK",
                    entity_id=task.id,
                    payload={
                        "title": task.title,
                        "project_id": str(task.project_id),
                        "assigned_to": (
                            str(task.assigned_to_id)
                            if task.assigned_to_id
                            else None
                        ),
                        "completed_by": str(self.request.user.id),
                        "completed_at": task.completed_at.isoformat(),
                    },
                )

        elif old_status == TaskModel.Status.COMPLETED:
            if task.completed_at is not None:
                task.completed_at = None
                task.save(update_fields=["completed_at"])

            publish_event(
                event_type="TASK_REOPENED",
                entity_type="TASK",
                entity_id=task.id,
                payload={
                    "title": task.title,
                    "project_id": str(task.project_id),
                    "assigned_to": (
                        str(task.assigned_to_id) if task.assigned_to_id else None
                    ),
                    "reopen_by": str(self.request.user.id),
                    "status": task.status,
                },
            )
