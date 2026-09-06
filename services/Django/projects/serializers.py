from rest_framework import serializers
from projects.models import ProjectModel


class ProjectSerializer(serializers.ModelSerializer):

    owner_id = serializers.UUIDField(source="owenr_id", read_only=True)
    class Meta:
        model = ProjectModel
        fields =  ["id", "name", "description", "owner_id", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "owner_id"]