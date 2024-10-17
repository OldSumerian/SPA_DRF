from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User


# python manage.py test - запуск тестов
# python manage.py test users.tests.tests_user - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными строками


class UserTestCaseAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя и его же
    доступ к своим же данным"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.user1 = User.objects.create(email="user1@my.ru")
        self.client.force_authenticate(user=self.user)

    def test_user_str(self):
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(str(user), user.email)

    def test_user_create(self):
        data = {"email": "user2@my.ru", "password": "password"}
        response = self.client.post(reverse("users:users-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.last()
        self.assertEqual(user.email, data["email"])

    def test_user_create_without_email(self):
        data = {"name": "user2@my.ru", "password": "password"}
        response = self.client.post(reverse("users:users-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_list(self):
        response = self.client.get(reverse("users:users-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            [
                {"id": self.user.pk, "email": self.user.email},
                {"id": self.user1.pk, "email": self.user1.email},
            ],
        )

    def test_course_retrieve_self(self):
        response = self.client.get(
            reverse("users:users-detail", args=(self.user.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["is_staff"], False)
        self.assertEqual(data["is_active"], True)

    def test_course_retrieve_another(self):
        response = self.client.get(
            reverse("users:users-detail", args=(self.user1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(
            data, {"id": self.user1.pk, "email": self.user1.email}
        )

    def test_user_update_self(self):
        data = {"email": "new_email@my.ru"}
        response = self.client.patch(
            reverse("users:users-detail", args=(self.user.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.email, data["email"])

    def test_user_update_another(self):
        data = {"email": "new_email1@my.ru"}
        response = self.client.patch(
            reverse("users:users-detail", args=(self.user1.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user = User.objects.get(pk=self.user1.pk)
        self.assertEqual(user.email, self.user1.email)

    def test_course_delete_self(self):
        response = self.client.delete(
            reverse("users:users-detail", args=(self.user.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_course_delete_another(self):
        response = self.client.delete(
            reverse("users:users-detail", args=(self.user1.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=self.user1.pk).exists())


class UserTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают не авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")

    def test_user_create(self):
        data = {"email": "user2@my.ru", "password": "password"}
        response = self.client.post(reverse("users:users-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.last()
        self.assertEqual(user.email, data["email"])

    def test_user_list(self):
        response = self.client.get(reverse("users:users-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_retrieve(self):
        response = self.client.get(
            reverse("users:users-detail", args=(self.user.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update(self):
        data = {"email": "new_email@my.ru"}
        response = self.client.patch(
            reverse("users:users-detail", args=(self.user.pk,)), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_delete_self(self):
        response = self.client.delete(
            reverse("users:users-detail", args=(self.user.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestJWTTestCase(APITestCase):

    def setUp(self):
        User.objects.create_user(email="user@my.ru", password="pass")

    def test_jwt_token(self):
        data = {"email": "user@my.ru", "password": "pass"}
        response = self.client.post(reverse("users:token"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # access refresh
        data = response.json()
        self.assertTrue("access" in data)
        self.assertTrue("refresh" in data)
        refresh_token = data["refresh"]

        token_refresh_url = reverse("users:token_refresh")
        resp = self.client.post(
            token_refresh_url, {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(
            token_refresh_url, {"refresh": "abc"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
