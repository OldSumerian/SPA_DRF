from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from spa.models import Habit, Place, Action
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test spa.tests.tests_habit - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class HabitTestCaseCreateValidationAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя и
    его же доступ к своим же данным"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.place = Place.objects.create(name="Дом")
        self.action = Action.objects.create(name="Пробежка")
        # self.course = Habit.objects.create(
        #     user=self.user,
        #     place=self.place,
        #     action=self.action,
        #     date_time=datetime.datetime(1997, 10, 19, 12, 0, 0),
        #     is_pleasant=False,
        #     related_habit=None,
        #     period=PERIOD_EVERY_DAY,
        #     reward="Бургер",
        #     time_to_complete=100,
        #     is_public=False
        # )
        self.client.force_authenticate(user=self.user)

    def add_pleasant_habit(self) -> Habit:
        habit = Habit.objects.create(
            user=self.user,
            place=self.place,
            action=self.action,
            date_time=timezone.datetime(
                1997, 10, 19, 12, 0, 0, tzinfo=timezone.get_current_timezone()
            ),
            is_pleasant=True,
            period=Habit.PERIOD_EVERY_DAY,
            time_to_complete=100,
            is_public=False,
        )
        return habit

    def test_str(self):
        habit = self.add_pleasant_habit()
        self.assertEqual(
            str(habit),
            f"{habit.user.email}: {habit.place.name}, {habit.action.name}",
        )

    def test_create_valid_habit(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            # "related_habit": None,
            "period": Habit.PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.last()
        self.assertEqual(habit.place.pk, data["place"])
        self.assertEqual(habit.user, self.user)

    def test_create_not_valid_period_choices(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            # "related_habit": None,
            "period": "ANY_PERIOD",
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 0)

    def test_create_not_valid_habit_time_to_complete(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "period": Habit.PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 121,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 0)

    def test_create_not_valid_habit_only_related_or_reward(self):
        related_habit = self.add_pleasant_habit()
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "related_habit": related_habit.pk,
            "period": Habit.PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

    def test_create_not_valid_habit_is_pleasant(self):
        related_habit = self.add_pleasant_habit()

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": True,
            "related_habit": related_habit.pk,
            "period": Habit.PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": True,
            "related_habit": related_habit.pk,
            "period": Habit.PERIOD_EVERY_DAY,
            # "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": True,
            # "related_habit": related_habit.pk,
            "period": Habit.PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": True,
            # "related_habit": related_habit.pk,
            "period": Habit.PERIOD_EVERY_DAY,
            # "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_create_not_valid_related_only_pleasant(self):
        related_habit = self.add_pleasant_habit()
        related_habit.is_pleasant = False
        related_habit.save()

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "related_habit": related_habit.pk,
            "period": Habit.PERIOD_EVERY_DAY,
            # "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 1)

        related_habit.is_pleasant = True
        related_habit.save()

        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "related_habit": related_habit.pk,
            "period": Habit.PERIOD_EVERY_DAY,
            # "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)


class HabitTestCaseCreateDifferentUsers(APITestCase):
    """Данные тесты описывают авторизованного пользователя
    и его же доступ к своим же данным"""

    def setUp(self) -> None:
        self.user1 = User.objects.create(email="user1@my.ru")
        self.user2 = User.objects.create(email="user2@my.ru")
        self.user3 = User.objects.create(email="user3@my.ru")

        self.place = Place.objects.create(name="Дом")
        self.action = Action.objects.create(name="Пробежка")
        self.habit_user1 = Habit.objects.create(
            user=self.user1,
            place=self.place,
            action=self.action,
            date_time=timezone.datetime(
                1997, 10, 19, 12, 0, 0, tzinfo=timezone.get_current_timezone()
            ),
            is_pleasant=False,
            related_habit=None,
            period=Habit.PERIOD_EVERY_DAY,
            reward="Бургер",
            time_to_complete=100,
            is_public=False,
        )

        self.habit_user2 = Habit.objects.create(
            user=self.user2,
            place=self.place,
            action=self.action,
            date_time=timezone.datetime(
                1997, 10, 19, 12, 0, 0, tzinfo=timezone.get_current_timezone()
            ),
            is_pleasant=False,
            related_habit=None,
            period=Habit.PERIOD_EVERY_DAY,
            reward="Бургер",
            time_to_complete=110,
            is_public=False,
        )

        self.habit_public_user2 = Habit.objects.create(
            user=self.user2,
            place=self.place,
            action=self.action,
            date_time=timezone.datetime(
                1997, 10, 19, 12, 0, 0, tzinfo=timezone.get_current_timezone()
            ),
            is_pleasant=False,
            related_habit=None,
            period=Habit.PERIOD_EVERY_DAY,
            reward="Бургер",
            time_to_complete=110,
            is_public=True,
        )

    def test_not_authenticated_create(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "period": Habit.PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_authenticated_my_list(self):
        response = self.client.get(reverse("spa:habit-list-my"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_authenticated_public_list(self):
        response = self.client.get(reverse("spa:habit-list-public"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_authenticated_retrieve(self):
        response = self.client.get(
            reverse("spa:habit-retrieve", args=(self.habit_user1.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_authenticated_update(self):
        data = {
            "reward": "Сон",
        }
        response = self.client.patch(
            reverse("spa:habit-update", args=(self.habit_user1.pk,)), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_authenticated_delete(self):
        response = self.client.delete(
            reverse("spa:habit-update", args=(self.habit_user1.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_my_list(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse("spa:habit-list-my"))
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["id"], self.habit_user1.pk)
        self.assertEqual(data["results"][0]["user"], self.user1.pk)

    def test_authenticated_public_list(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse("spa:habit-list-public"))
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["id"], self.habit_public_user2.pk)
        self.assertEqual(data["results"][0]["user"], self.user2.pk)
        self.assertEqual(
            data["results"][0]["is_public"], self.habit_public_user2.is_public
        )

    def test_authenticated_my_retrieve(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse("spa:habit-retrieve", args=(self.habit_user1.pk,))
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["id"], self.habit_user1.pk)
        self.assertEqual(data["user"], self.user1.pk)

    def test_authenticated_other_retrieve(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse("spa:habit-retrieve", args=(self.habit_user2.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_other_public_retrieve(self):
        """Так как в ТЗ
        Пользователь может видеть список публичных привычек
        без возможности их как-то редактировать или удалять.
        Так как ТОЛЬКО список, то через retrieve доступ закрыт"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            reverse("spa:habit-retrieve", args=(self.habit_public_user2.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_my_update(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "reward": "Сон",
        }
        response = self.client.patch(
            reverse("spa:habit-update", args=(self.habit_user1.pk,)), data=data
        )
        resp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(resp_data["id"], self.habit_user1.pk)
        self.assertEqual(resp_data["user"], self.user1.pk)
        self.assertEqual(resp_data["reward"], data["reward"])

    def test_authenticated_other_update(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "reward": "Сон",
        }
        response = self.client.patch(
            reverse("spa:habit-update", args=(self.habit_user2.pk,)), data=data
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_other_public_update(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "reward": "Сон",
        }
        response = self.client.patch(
            reverse("spa:habit-update", args=(self.habit_public_user2.pk,)),
            data=data,
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_my_delete(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(
            reverse("spa:habit-delete", args=(self.habit_user1.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit_user1.pk).exists())

    def test_authenticated_other_delete(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(
            reverse("spa:habit-delete", args=(self.habit_user2.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_other_public_delete(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(
            reverse("spa:habit-delete", args=(self.habit_public_user2.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HabitTestCaseCreateWithAnyPeriod(APITestCase):
    """Данные тесты описывают создание привычки
    с разными периодами выполнения"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.place = Place.objects.create(name="Дом")
        self.action = Action.objects.create(name="Пробежка")
        self.client.force_authenticate(user=self.user)

    def test_create_disable(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "period": Habit.PERIOD_DISABLE,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.last()
        self.assertEqual(habit.date_time_next_sent, None)

    @freeze_time("2024-01-14 03:21:34", tz_offset=0)
    def test_create_every_minute(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "period": Habit.PERIOD_EVERY_MINUTE,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.last()
        self.assertEqual(
            habit.date_time_next_sent,
            timezone.datetime(
                2024, 1, 14, 3, 22, tzinfo=timezone.timezone.utc
            ),
        )

    @freeze_time("2024-01-14 03:21:34", tz_offset=0)
    def test_create_every_hour(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "period": Habit.PERIOD_EVERY_HOUR,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.last()
        self.assertEqual(
            habit.date_time_next_sent,
            timezone.datetime(2024, 1, 14, 4, 0, tzinfo=timezone.timezone.utc),
        )

    @freeze_time("2024-01-14 03:21:34", tz_offset=0)
    def test_create_every_day(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "period": Habit.PERIOD_EVERY_DAY,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.last()
        self.assertEqual(
            habit.date_time_next_sent,
            timezone.datetime(
                2024, 1, 14, 12, 0, tzinfo=timezone.timezone.utc
            ),
        )

    @freeze_time("2024-01-15 03:21:34", tz_offset=0)
    def test_create_every_week(self):
        data = {
            "place": self.place.pk,
            "action": self.action.pk,
            "date_time": "1997-10-19 12:00:00",
            "is_pleasant": False,
            "period": Habit.PERIOD_EVERY_WEEK,
            "reward": "Бургер",
            "time_to_complete": 120,
            "is_public": False,
        }
        response = self.client.post(reverse("spa:habit-create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit = Habit.objects.last()
        self.assertEqual(
            habit.date_time_next_sent,
            timezone.datetime(
                2024, 1, 21, 12, 0, tzinfo=timezone.timezone.utc
            ),
        )
