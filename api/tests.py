from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Task


class AuthTests(APITestCase):
    def test_register_returns_token(self):
        res = self.client.post(
            "/api/register/",
            {"username": "hetvi", "email": "h@example.com", "password": "pass1234"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", res.data)
        self.assertTrue(User.objects.filter(username="hetvi").exists())

    def test_register_duplicate_username_fails(self):
        User.objects.create_user("hetvi", password="pass1234")
        res = self.client.post(
            "/api/register/", {"username": "hetvi", "password": "pass1234"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password_fails(self):
        res = self.client.post(
            "/api/register/", {"username": "abc", "password": "123"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_token(self):
        User.objects.create_user("hetvi", password="pass1234")
        res = self.client.post(
            "/api/login/", {"username": "hetvi", "password": "pass1234"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_login_wrong_password_fails(self):
        User.objects.create_user("hetvi", password="pass1234")
        res = self.client.post(
            "/api/login/", {"username": "hetvi", "password": "wrong"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_deletes_token(self):
        user = User.objects.create_user("hetvi", password="pass1234")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        res = self.client.post("/api/logout/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=user).exists())


class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("hetvi", password="pass1234")
        self.other = User.objects.create_user("other", password="pass1234")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_tasks_require_token(self):
        self.client.credentials()  # remove the token
        res = self.client.get("/api/tasks/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        res = self.client.post(
            "/api/tasks/", {"title": "Learn Django", "description": "DRF basics"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.get(id=res.data["id"]).user, self.user)

    def test_create_task_without_title_fails(self):
        res = self.client.post("/api/tasks/", {"description": "no title"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_shows_only_own_tasks(self):
        Task.objects.create(user=self.user, title="Mine")
        Task.objects.create(user=self.other, title="Not mine")
        res = self.client.get("/api/tasks/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [t["title"] for t in res.data]
        self.assertEqual(titles, ["Mine"])

    def test_update_task(self):
        task = Task.objects.create(user=self.user, title="Old")
        res = self.client.put(
            "/api/tasks/%d/" % task.id,
            {"title": "New", "description": "", "is_completed": True},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "New")
        self.assertTrue(task.is_completed)

    def test_partial_update_task(self):
        task = Task.objects.create(user=self.user, title="Task")
        res = self.client.patch("/api/tasks/%d/" % task.id, {"is_completed": True}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

    def test_delete_task(self):
        task = Task.objects.create(user=self.user, title="Delete me")
        res = self.client.delete("/api/tasks/%d/" % task.id)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_cannot_access_other_users_task(self):
        task = Task.objects.create(user=self.other, title="Secret")
        self.assertEqual(
            self.client.get("/api/tasks/%d/" % task.id).status_code, status.HTTP_404_NOT_FOUND
        )
        self.assertEqual(
            self.client.delete("/api/tasks/%d/" % task.id).status_code, status.HTTP_404_NOT_FOUND
        )
        self.assertTrue(Task.objects.filter(id=task.id).exists())
