from django.db import models
from django.utils import timezone

from spa.services import (
    get_next_day_date,
    get_next_week_date,
    get_next_minute_date,
    get_next_hour_date,
)
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Place(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название места")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Пользователь",
        related_name="places",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Action(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название действия")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Пользователь",
        related_name="actions",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"


class Habit(models.Model):
    PERIOD_DISABLE = "DISABLE"
    PERIOD_EVERY_MINUTE = "EVERY_MINUTE"
    PERIOD_EVERY_HOUR = "EVERY_HOUR"
    PERIOD_EVERY_DAY = "EVERY_DAY"
    PERIOD_EVERY_WEEK = "EVERY_WEEK"

    PERIOD_CHOICES = {
        PERIOD_DISABLE: "Отключено",
        PERIOD_EVERY_MINUTE: "Ежеминутно",
        PERIOD_EVERY_HOUR: "Ежечасно",
        PERIOD_EVERY_DAY: "Ежедневно",
        PERIOD_EVERY_WEEK: "Еженедельно",
    }

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Пользователь",
        related_name="habits",
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Место",
        related_name="habits",
    )
    action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Действие",
        related_name="habits",
    )

    date_time = models.DateTimeField(verbose_name="Время выполнения")

    is_pleasant = models.BooleanField(
        verbose_name="Это приятная привычка", default=False
    )

    related_habit = models.ForeignKey(
        "Habit",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Связанная привычка",
    )

    period = models.CharField(
        max_length=30,
        verbose_name="периодичность",
        choices=PERIOD_CHOICES,
        default="DISABLE",
    )

    reward = models.CharField(
        max_length=150, verbose_name="Вознаграждение", default=""
    )

    time_to_complete = models.PositiveIntegerField(
        verbose_name="Время на выполнение, c", default=120
    )

    is_public = models.BooleanField(
        verbose_name="Признак публичности", default=False
    )

    # заполняется программно в алгоритме
    date_time_next_sent = models.DateTimeField(
        verbose_name="Дата и время следующего оповещения", **NULLABLE
    )

    def __str__(self):
        return f"{self.user.email}: {self.place.name}, {self.action.name}"

    def set_next_execution_time(self):
        date_time_start = self.date_time.replace(second=0, microsecond=0)
        now_time = timezone.now().replace(second=0, microsecond=0)

        match self.period:
            case self.PERIOD_EVERY_MINUTE:
                self.date_time_next_sent = get_next_minute_date(
                    date_time_start, now_time
                )

            case self.PERIOD_EVERY_HOUR:
                self.date_time_next_sent = get_next_hour_date(
                    date_time_start, now_time
                )

            case self.PERIOD_EVERY_DAY:
                self.date_time_next_sent = get_next_day_date(
                    date_time_start, now_time
                )

            case self.PERIOD_EVERY_WEEK:
                self.date_time_next_sent = get_next_week_date(
                    date_time_start, now_time
                )

            case _:
                pass

        self.save()

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
