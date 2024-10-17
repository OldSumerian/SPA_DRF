from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from spa.models import Place
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test spa.tests.tests_place - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class PlaceTestCaseAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.client.force_authenticate(user=self.user)
        self.place = Place.objects.create(name="Работа", user=self.user)

    def test_str(self):
        place = Place.objects.get(pk=self.place.pk)
        self.assertEqual(str(place), place.name)

    def test_create(self):
        data = {"name": "дом"}
        response = self.client.post(reverse("spa:places-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        place = Place.objects.last()
        self.assertEqual(place.name, data["name"])
        self.assertEqual(place.user, self.user)

    def test_retrieve(self):
        response = self.client.get(
            reverse("spa:places-detail", args=(self.place.pk,))
        )

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["name"], self.place.name)

    def test_list(self):
        response = self.client.get(reverse("spa:places-list"))

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data[0]["name"], self.place.name)

    def test_update(self):
        data = {"name": "Приседание updated"}
        response = self.client.patch(
            reverse("spa:places-detail", args=(self.place.pk,)), data=data
        )

        data_resp = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data_resp["name"], data["name"])

    def test_delete(self):
        response = self.client.delete(
            reverse("spa:places-detail", args=(self.place.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Place.objects.filter(pk=self.place.pk).exists())


class PlaceTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают не авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        # self.client.force_authenticate(user=self.user)
        self.place = Place.objects.create(name="Пробежка", user=self.user)

    def test_create(self):
        data = {"name": "Приседание"}
        response = self.client.post(reverse("spa:places-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve(self):
        response = self.client.get(
            reverse("spa:places-detail", args=(self.place.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        response = self.client.get(reverse("spa:places-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update(self):
        data = {"name": "Приседание updated"}
        response = self.client.patch(
            reverse("spa:places-detail", args=(self.place.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        response = self.client.delete(
            reverse("spa:places-detail", args=(self.place.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PlaceTestCaseAnotherUserAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.user2 = User.objects.create(email="user2@my.ru")
        self.client.force_authenticate(user=self.user2)
        self.place = Place.objects.create(name="Пробежка", user=self.user)

    def test_retrieve(self):
        response = self.client.get(
            reverse("spa:places-detail", args=(self.place.pk,))
        )

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["name"], self.place.name)

    def test_list(self):
        response = self.client.get(reverse("spa:places-list"))

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data[0]["name"], self.place.name)

    def test_update(self):
        data = {"name": "Приседание updated"}
        response = self.client.patch(
            reverse("spa:places-detail", args=(self.place.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        response = self.client.delete(
            reverse("spa:places-detail", args=(self.place.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
