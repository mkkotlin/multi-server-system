from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()


    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    # def get_serializer_class(self):
    #     if self.action == "create":
    #         return UserCreateSerializer
    #     return UserSerializer

    # def update(self, request, *args, **kwargs):
    #     return Response({"message": "Ristricted update features"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

    # def destroy(self, request, *args, **kwargs):
    #     return Response({"message": "Ristricted delete features"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)