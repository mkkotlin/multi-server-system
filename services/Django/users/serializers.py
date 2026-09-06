from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active", "created_at", "updated_at", ]
        read_only_fields = ["id", "created_at", "updated_at", "is_active", "role"]



class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ["username", "email", "password",]
        # read_only_fields = ["role", "is_active"]   
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, role=User.Role.USER ,**validated_data)
        return user