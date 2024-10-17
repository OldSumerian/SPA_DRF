from django.utils import timezone
from rest_framework.test import APITestCase

from spa.services import (
    get_next_day_date,
    get_next_week_date,
    get_next_hour_date,
    get_next_minute_date,
)


# python manage.py test - запуск тестов
# python manage.py test spa.tests.tests_services - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class HabitTestCaseCreateValidationAuthenticated(APITestCase):
    def setUp(self) -> None:
        pass

    def test_get_next_minute_date(self):
        date_time_start_sent = timezone.datetime.fromisoformat(
            "2024-05-28T16:15:34"
        )

        now_time = timezone.datetime.fromisoformat("2024-04-15T18:10:01")
        self.assertEqual(
            str(get_next_minute_date(date_time_start_sent, now_time)),
            "2024-05-28 16:15:00",
        )

        now_time = timezone.datetime.fromisoformat("2024-06-15T13:10:01")
        self.assertEqual(
            str(get_next_minute_date(date_time_start_sent, now_time)),
            "2024-06-15 13:11:00",
        )

        now_time = timezone.datetime.fromisoformat("2024-06-15T18:10:01")
        self.assertEqual(
            str(get_next_minute_date(date_time_start_sent, now_time)),
            "2024-06-15 18:11:00",
        )

    def test_get_next_hour_date(self):
        date_time_start_sent = timezone.datetime.fromisoformat(
            "2024-05-28T16:15:34"
        )

        now_time = timezone.datetime.fromisoformat("2024-04-15T18:10:01")
        self.assertEqual(
            str(get_next_hour_date(date_time_start_sent, now_time)),
            "2024-05-28 16:15:00",
        )

        now_time = timezone.datetime.fromisoformat("2024-06-15T13:10:01")
        self.assertEqual(
            str(get_next_hour_date(date_time_start_sent, now_time)),
            "2024-06-15 13:15:00",
        )

        now_time = timezone.datetime.fromisoformat("2024-06-15T18:10:01")
        self.assertEqual(
            str(get_next_hour_date(date_time_start_sent, now_time)),
            "2024-06-15 18:15:00",
        )

    def test_get_next_day_date(self):
        date_time_start_sent = timezone.datetime.fromisoformat(
            "2024-05-28T16:15:34"
        )

        now_time = timezone.datetime.fromisoformat("2024-04-15T18:10:01")
        self.assertEqual(
            str(get_next_day_date(date_time_start_sent, now_time)),
            "2024-05-28 16:15:00",
        )

        now_time = timezone.datetime.fromisoformat("2024-06-15T13:10:01")
        self.assertEqual(
            str(get_next_day_date(date_time_start_sent, now_time)),
            "2024-06-15 16:15:00",
        )

        now_time = timezone.datetime.fromisoformat("2024-06-15T18:10:01")
        self.assertEqual(
            str(get_next_day_date(date_time_start_sent, now_time)),
            "2024-06-16 16:15:00",
        )

    def test_get_next_week_date(self):
        date_time_start_sent = timezone.datetime.fromisoformat(
            "2024-05-28T16:15:34"
        )

        now_time = timezone.datetime.fromisoformat("2024-04-15T18:10:01")
        self.assertEqual(
            str(get_next_week_date(date_time_start_sent, now_time)),
            "2024-05-28 16:15:00",
        )

        now_time = timezone.datetime.fromisoformat("2024-06-15T13:10:01")
        self.assertEqual(
            str(get_next_week_date(date_time_start_sent, now_time)),
            "2024-06-18 16:15:00",
        )

        now_time = timezone.datetime.fromisoformat("2024-06-15T18:10:01")
        self.assertEqual(
            str(get_next_week_date(date_time_start_sent, now_time)),
            "2024-06-18 16:15:00",
        )
