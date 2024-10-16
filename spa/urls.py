from django.urls import path
from rest_framework.routers import DefaultRouter

from spa.apps import SpaConfig
from spa.views import (
    PlaceViewSet,
    ActionViewSet,
    HabitCreateAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitDeleteAPIView,
    HabitPublicListAPIView,
)

app_name = SpaConfig.name

place_router = DefaultRouter()
action_router = DefaultRouter()
place_router.register(r"places", PlaceViewSet, basename="places")
action_router.register(r"actions", ActionViewSet, basename="actions")

urlpatterns = (
    [
        path(
            "habit/create/", HabitCreateAPIView.as_view(), name="habit-create"
        ),
        path(
            "habit/list/my/", HabitListAPIView.as_view(), name="habit-list-my"
        ),
        path(
            "habit/list/public/",
            HabitPublicListAPIView.as_view(),
            name="habit-list-public",
        ),
        path(
            "habit/<int:pk>/",
            HabitRetrieveAPIView.as_view(),
            name="habit-retrieve",
        ),
        path(
            "habit/update/<int:pk>/",
            HabitUpdateAPIView.as_view(),
            name="habit-update",
        ),
        path(
            "habit/delete/<int:pk>/",
            HabitDeleteAPIView.as_view(),
            name="habit-delete",
        ),
    ]
    + place_router.urls
    + action_router.urls
)
