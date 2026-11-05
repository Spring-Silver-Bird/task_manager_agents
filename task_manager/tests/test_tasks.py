# task_manager/tests/test_tasks.py

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.status = Status.objects.create(name="TestStatus")
        self.labels = Label.objects.create(name="TestLabel")
        self.task = Task.objects.create(
            name="Test_task", description="some", status=self.status, author=self.user, executor=self.user
        )

    def test_list_guest(self):
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_detail_get_guest(self):
        response = self.client.get(reverse("tasks:detail", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_create_get_guest(self):
        response = self.client.get(reverse("tasks:create"))
        self.assertEqual(response.status_code, 302)

    def test_create_post_guest(self):
        count_before = Task.objects.count()
        response = self.client.post(
            reverse("tasks:create"),
            {"name": "New_task", "description": "new_description", "status": self.status.pk, "executor": self.user.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertEqual(Task.objects.count(), count_before)

    def test_update_get_guest(self):
        response = self.client.get(reverse("tasks:update", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)

    def test_update_post_guest(self):
        response = self.client.post(
            reverse("tasks:update", kwargs={"pk": self.task.pk}),
            {"name": "Hack", "status": self.status.pk, "executor": self.user.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.name, "Hack")

    def test_delete_get_guest(self):
        response = self.client.get(reverse("tasks:delete", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_post_guest(self):
        pk = self.task.pk
        response = self.client.post(reverse("tasks:delete", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=pk).exists())

    def test_task_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("tasks", response.context)

    def test_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:create"))
        self.assertEqual(response.status_code, 200)

    def test_create_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("tasks:create"),
            {
                "name": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertIn("name", response.context["form"].errors)
        self.assertEqual(Task.objects.count(), 1)
        self.assertFalse(Task.objects.filter(name="").exists())

    def test_create_valid(self):
        self.client.force_login(self.user)
        count_before = Task.objects.count()
        response = self.client.post(
            reverse("tasks:create"),
            {
                "name": "Valid",
                "description": "d",
                "status": self.status.pk,
                "executor": self.user.pk,
                "labels": [self.labels.pk],
            },
            follow=False,
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertEqual(Task.objects.count(), count_before + 1)
        task = Task.objects.get(name="Valid")
        self.assertEqual(task.author, self.user)
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.executor, self.user)
        self.assertTrue(Task.objects.filter(name="Valid").exists())
        self.assertEqual(Task.objects.get(name="Valid").author, self.user)
        self.assertIn(self.labels, task.labels.all())
        msgs = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Задача успешно создана", msgs)

    def test_update_get_own(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:update", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/update.html")
        self.assertContains(response, "Изменить")

    def test_update_post_own(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("tasks:update", kwargs={"pk": self.task.pk}),
            {"name": "other task", "description": "new", "status": self.status.pk, "executor": self.user.pk},
            follow=False,
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "other task")
        list_resp = self.client.get(reverse("tasks:list"))
        self.assertContains(list_resp, "other task")

    def test_update_other_allowed(self):
        other = User.objects.create_user(username="Lu-Tze", password="Sweeper1")
        self.client.force_login(other)
        response = self.client.get(reverse("tasks:update", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("tasks:update", kwargs={"pk": self.task.pk}),
            {"name": "Hack", "description": "some", "status": self.status.pk, "executor": self.user.pk},
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Hack")

    def test_delete_get_own(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:delete", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/delete.html")
        self.assertContains(response, "Да, удалить")

    def test_delete_post_own(self):
        self.client.force_login(self.user)
        pk = self.task.pk
        response = self.client.post(reverse("tasks:delete", kwargs={"pk": pk}))
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertFalse(Task.objects.filter(pk=pk).exists())
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_forbidden_other(self):
        other = User.objects.create_user(username="other2", password="pass12345")
        self.client.force_login(other)
        response = self.client.post(reverse("tasks:delete", kwargs={"pk": self.task.pk}))
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        msgs = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Задачу может удалить только ее автор", msgs)
