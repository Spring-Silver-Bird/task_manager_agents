from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status, StatusType
from task_manager.tasks.models import Task

User = get_user_model()


class AdminTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="RucticWitch",
            email="RucticWitch@example.com",
            password="StrongPassw0rd!",
        )
        self.user = User.objects.create_user(username="regular", password="StrongPassw0rd!")
        self.status = Status.objects.create(
            name="New",
            when_to_apply="When work starts",
            status_type=StatusType.IN_PROGRESS,
        )
        self.label = Label.objects.create(
            name="Bug",
            meaning="Broken behavior",
            karma_effect="Negative karma",
        )
        self.task = Task.objects.create(name="Task", status=self.status, author=self.superuser)
        self.task.labels.add(self.label)

    def test_admin_requires_login(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)

    def test_regular_user_has_no_admin_access(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)

    def test_superuser_can_open_changelists(self):
        self.client.force_login(self.superuser)
        for url_name in (
            "admin:tasks_task_changelist",
            "admin:statuses_status_changelist",
            "admin:labels_label_changelist",
            "admin:auth_user_changelist",
        ):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_status_admin_shows_new_fields(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("admin:statuses_status_changelist"))
        self.assertContains(response, "When work starts")
        self.assertContains(response, "In Progress")

    def test_label_admin_shows_new_fields(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("admin:labels_label_changelist"))
        self.assertContains(response, "Broken behavior")
        self.assertContains(response, "Negative karma")

    def test_superuser_can_delete_task(self):
        self.client.force_login(self.superuser)
        pk = self.task.pk
        response = self.client.post(
            reverse("admin:tasks_task_delete", args=[pk]),
            {"post": "yes"},
        )
        self.assertRedirects(response, reverse("admin:tasks_task_changelist"))
        self.assertFalse(Task.objects.filter(pk=pk).exists())

    def test_superuser_can_delete_label_used_by_task(self):
        self.client.force_login(self.superuser)
        pk = self.label.pk
        response = self.client.post(
            reverse("admin:labels_label_delete", args=[pk]),
            {"post": "yes"},
        )
        self.assertRedirects(response, reverse("admin:labels_label_changelist"))
        self.assertFalse(Label.objects.filter(pk=pk).exists())
        self.assertFalse(self.task.labels.exists())

    def test_superuser_cannot_delete_status_used_by_task(self):
        self.client.force_login(self.superuser)
        pk = self.status.pk
        response = self.client.post(
            reverse("admin:statuses_status_delete", args=[pk]),
            {"post": "yes"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Status.objects.filter(pk=pk).exists())

    def test_superuser_can_delete_user_without_tasks(self):
        self.client.force_login(self.superuser)
        pk = self.user.pk
        response = self.client.post(
            reverse("admin:auth_user_delete", args=[pk]),
            {"post": "yes"},
        )
        self.assertRedirects(response, reverse("admin:auth_user_changelist"))
        self.assertFalse(User.objects.filter(pk=pk).exists())

    def test_superuser_cannot_delete_user_with_tasks(self):
        self.client.force_login(self.superuser)
        author = User.objects.create_user(username="author", password="StrongPassw0rd!")
        Task.objects.create(name="Authored", status=self.status, author=author)
        pk = author.pk
        response = self.client.post(
            reverse("admin:auth_user_delete", args=[pk]),
            {"post": "yes"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(pk=pk).exists())
