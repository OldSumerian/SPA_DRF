from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from spa.models import Action
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test spa.tests.tests_action - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class ActionTestCaseAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.client.force_authenticate(user=self.user)
        self.action = Action.objects.create(name="Пробежка", user=self.user)

    def test_str(self):
        action = Action.objects.get(pk=self.action.pk)
        self.assertEqual(str(action), action.name)

    def test_create(self):
        data = {"name": "Приседание"}
        response = self.client.post(reverse("spa:actions-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        action = Action.objects.last()
        self.assertEqual(action.name, data["name"])
        self.assertEqual(action.user, self.user)

    def test_retrieve(self):
        response = self.client.get(
            reverse("spa:actions-detail", args=(self.action.pk,))
        )

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["name"], self.action.name)

    def test_list(self):
        response = self.client.get(reverse("spa:actions-list"))

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data[0]["name"], self.action.name)

    def test_update(self):
        data = {"name": "Приседание updated"}
        response = self.client.patch(
            reverse("spa:actions-detail", args=(self.action.pk,)), data=data
        )

        data_resp = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data_resp["name"], data["name"])

    def test_delete(self):
        response = self.client.delete(
            reverse("spa:actions-detail", args=(self.action.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Action.objects.filter(pk=self.action.pk).exists())


class ActionTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают не авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        # self.client.force_authenticate(user=self.user)
        self.action = Action.objects.create(name="Пробежка", user=self.user)

    def test_create(self):
        data = {"name": "Приседание"}
        response = self.client.post(reverse("spa:actions-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve(self):
        response = self.client.get(
            reverse("spa:actions-detail", args=(self.action.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        response = self.client.get(reverse("spa:actions-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update(self):
        data = {"name": "Приседание updated"}
        response = self.client.patch(
            reverse("spa:actions-detail", args=(self.action.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        response = self.client.delete(
            reverse("spa:actions-detail", args=(self.action.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ActionTestCaseAnotherUserAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.user2 = User.objects.create(email="user2@my.ru")
        self.client.force_authenticate(user=self.user2)
        self.action = Action.objects.create(name="Пробежка", user=self.user)

    def test_retrieve(self):
        response = self.client.get(
            reverse("spa:actions-detail", args=(self.action.pk,))
        )

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["name"], self.action.name)

    def test_list(self):
        response = self.client.get(reverse("spa:actions-list"))

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data[0]["name"], self.action.name)

    def test_update(self):
        data = {"name": "Приседание updated"}
        response = self.client.patch(
            reverse("spa:actions-detail", args=(self.action.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        response = self.client.delete(
            reverse("spa:actions-detail", args=(self.action.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
