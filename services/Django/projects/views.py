from rest_framework import viewsets
from projects.models import ProjectModel
from projects.serializers import ProjectSerializer
from projects.permissions import IsProjectOwnerOrAdmin

# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwnerOrAdmin]


    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return ProjectModel.objects.select_related("owner").all()

        return ProjectModel.objects.select_related("owner").filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)