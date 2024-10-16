"""
Валидаторы
+ Исключить одновременный выбор связанной привычки и указания вознаграждения.
+ В модели не должно быть заполнено одновременно и поле вознаграждения,
+ и поле связанной привычки. Можно заполнить только одно из двух полей.

+ Время выполнения должно быть не больше 120 секунд.

+ В связанные привычки могут попадать только привычки с
+ признаком приятной привычки.

+ У приятной привычки не может быть вознаграждения или связанной привычки.

? Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
Нельзя не выполнять привычку более 7 дней. Например,
привычка может повторяться раз в неделю, но не раз в 2 недели.
За одну неделю необходимо выполнить привычку хотя бы один раз.
"""

from rest_framework import serializers

from spa.models import Habit

MAXIMUM_TIME_TO_HABIT_COMPLETE = (
    120  # Максимальное время выполнения привычки (по ТЗ 120 сек)
)


class SelectOnlyRelatedHabitOrRewardValidator:
    """Валидатор исключает одновременный выбор связанной привычки
    и указания вознаграждения."""

    def __init__(self, related_habit_field, reward_field):
        self.related_habit_field = related_habit_field
        self.reward_field = reward_field

    def __call__(self, value: dict):
        related_habit = value.get(self.related_habit_field, None)
        reward = value.get(self.reward_field, "")
        if related_habit is not None and reward != "":
            raise serializers.ValidationError(
                "Нельзя указать связанную привычку и "
                "вознаграждение одновременно"
            )


class TimeToHabitCompleteValidator:
    """Валидатор проверяет время на выполнение привычки
    (не более MAXIMUM_TIME_TO_HABIT_COMPLETE)"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value: dict):
        if self.field in value:
            if value.get(self.field, 0) > MAXIMUM_TIME_TO_HABIT_COMPLETE:
                raise serializers.ValidationError(
                    f"Время на выполнение привычки указано больше чем "
                    f"{MAXIMUM_TIME_TO_HABIT_COMPLETE} секунд"
                )


class IsPleasantHabitValidator:
    """Валидатор проверяет, что у приятной привычки
    не может быть вознаграждения или связанной привычки."""

    def __init__(self, field, related_fields):
        self.field = field
        self.related_fields = related_fields

    def __call__(self, value: dict):
        if value.get(self.field, False):
            for field in self.related_fields:
                related_value = value.get(field, None)
                if not (related_value is None or related_value == ""):
                    raise serializers.ValidationError(
                        "У приятной привычки не может быть вознаграждения "
                        "или связанной привычки"
                    )


class RelatedHabitValidator:
    """Валидатор проверяет, что в связанную привычку
    попадает только привычка с признаком приятной привычки."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value: dict):
        related_habit = value.get(self.field, None)
        if related_habit is not None:
            if not related_habit.is_pleasant:
                raise serializers.ValidationError(
                    "Связанная привычка должна быть приятной"
                )


class PeriodChoicesValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if self.field in value:
            period = value.get(self.field)
            if period not in Habit.PERIOD_CHOICES.keys():
                raise serializers.ValidationError(
                    f'Периодичность может быть только из списка: {", ".join(Habit.PERIOD_CHOICES.keys())}'
                )
