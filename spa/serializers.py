import spa.validators
from rest_framework import serializers

from spa.models import Place, Action, Habit


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            spa.validators.SelectOnlyRelatedHabitOrRewardValidator(
                related_habit_field="related_habit", reward_field="reward"
            ),
            spa.validators.TimeToHabitCompleteValidator(
                field="time_to_complete"
            ),
            spa.validators.IsPleasantHabitValidator(
                field="is_pleasant", related_fields=("related_habit", "reward")
            ),
            spa.validators.RelatedHabitValidator(field="related_habit"),
            spa.validators.PeriodChoicesValidator(field="period"),
        ]
