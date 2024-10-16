from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsSelfProfile
from users.serializers import (
    UserSerializer,
    UserShortSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Специально сохраняем получаемый объект,
        # для получения нужного сериализатора
        self.user_obj = obj
        return obj

    def get_serializer_class(self):
        if self.action == "list":
            return UserShortSerializer
        elif self.action == "retrieve":
            # Выбираем нужный сериализатор, исходя из совпадающего pk
            if self.request.user == self.user_obj:
                return UserSerializer
            else:
                return UserShortSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [
                AllowAny,
            ]
        elif self.action in ("list", "retrieve"):
            self.permission_classes = [
                IsAuthenticated,
            ]
        else:
            self.permission_classes = [
                IsSelfProfile,
            ]
        return super().get_permissions()
