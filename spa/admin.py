from django.contrib import admin

from spa.models import Place, Action, Habit


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_filter = ("name",)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_filter = ("name",)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "place",
        "action",
        "date_time",
        "is_pleasant",
        "related_habit",
        "period",
        "reward",
        "time_to_complete",
        "is_public",
        "date_time_next_sent",
    )
    list_filter = ("user", "place", "action")
