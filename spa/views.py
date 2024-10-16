from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from spa.models import Habit, Place, Action
from spa.paginators import CustomPagePagination
from spa.serializers import HabitSerializer, PlaceSerializer, ActionSerializer
from users.permissions import IsOwner


class PlaceViewSet(viewsets.ModelViewSet):
    """Место выполнения привычки"""

    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        obj.save()

    def get_permissions(self):
        if self.action in ("create", "retrieve", "list"):
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class ActionViewSet(viewsets.ModelViewSet):
    """Действия привычки"""

    serializer_class = ActionSerializer
    queryset = Action.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        obj.save()

    def get_permissions(self):
        if self.action in ("create", "retrieve", "list"):
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        obj.set_next_execution_time()
        obj.save()


class HabitListAPIView(generics.ListAPIView):
    """Просмотр своих привычек"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = CustomPagePagination
    queryset = Habit.objects.all().order_by("id")

    def get_queryset(self):
        # возврат кверисета для текущего пользователя
        return self.queryset.filter(user=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """Просмотр всех публичных привычек"""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagePagination
    queryset = Habit.objects.all().filter(is_public=True).order_by("id")


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр конкретной привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Обновление привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        habit = serializer.save()
        habit.set_next_execution_time()
        habit.save()


class HabitDeleteAPIView(generics.DestroyAPIView):
    """Удаление привычки"""

    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
