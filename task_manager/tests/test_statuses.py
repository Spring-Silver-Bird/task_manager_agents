# task_manager/tests/test_statuses.py

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class StatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.status = Status.objects.create(name="Test")

    def test_list_guest(self):
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_create_get_guest(self):
        response = self.client.get(reverse("statuses:create"))
        self.assertEqual(response.status_code, 302)

    def test_create_post_guest(self):
        count_before = Status.objects.count()
        response = self.client.post(reverse("statuses:create"), {"name": "New"})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertEqual(Status.objects.count(), count_before)

    def test_update_get_guest(self):
        response = self.client.get(reverse("statuses:update", kwargs={"pk": self.status.pk}))
        self.assertEqual(response.status_code, 302)

    def test_update_post_guest(self):
        response = self.client.post(reverse("statuses:update", kwargs={"pk": self.status.pk}), {"name": "Hack"})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertNotEqual(self.status.name, "Hack")

    def test_delete_get_guest(self):
        response = self.client.get(reverse("statuses:delete", kwargs={"pk": self.status.pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_post_guest(self):
        pk = self.status.pk
        response = self.client.post(reverse("statuses:delete", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(pk=pk).exists())

    def test_status_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("statuses", response.context)

    def test_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses:create"))
        self.assertEqual(response.status_code, 200)

    def test_create_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("statuses:create"),
            {
                "name": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertIn("name", response.context["form"].errors)
        self.assertEqual(Status.objects.count(), 1)
        self.assertFalse(Status.objects.filter(name="").exists())

    def test_update_get_own(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses:update", kwargs={"pk": self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/update.html")
        self.assertContains(response, "Изменить")

    def test_update_post_own(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("statuses:update", kwargs={"pk": self.status.pk}), {"name": "in progress"}, follow=False
        )
        self.assertRedirects(response, reverse("statuses:list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "in progress")
        list_resp = self.client.get(reverse("statuses:list"))
        self.assertContains(list_resp, "in progress")

    def test_update_other_allowed(self):
        other = User.objects.create_user(username="Lu-Tze", password="Sweeper1")
        self.client.force_login(other)
        response = self.client.get(reverse("statuses:update", kwargs={"pk": self.status.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("statuses:update", kwargs={"pk": self.status.pk}), {"name": "Hack"})
        self.assertRedirects(response, reverse("statuses:list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Hack")

    def test_delete_get_own(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses:delete", kwargs={"pk": self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/delete.html")
        self.assertContains(response, "Да, удалить")

    def test_delete_post_own(self):
        self.client.force_login(self.user)
        pk = self.status.pk
        response = self.client.post(reverse("statuses:delete", kwargs={"pk": pk}))
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertFalse(Status.objects.filter(pk=pk).exists())
        self.assertEqual(Status.objects.count(), 0)

    def test_delete_protected(self):
        self.client.force_login(self.user)
        Task.objects.create(name="T1", description="d", status=self.status, author=self.user, executor=self.user)
        response = self.client.post(reverse("statuses:delete", kwargs={"pk": self.status.pk}))
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
        resp2 = self.client.post(reverse("statuses:delete", kwargs={"pk": self.status.pk}), follow=True)
        self.assertContains(resp2, "Невозможно удалить статус")

    def test_delete_other_allowed(self):
        other = User.objects.create_user(username="other2", password="pass12345")
        self.client.force_login(other)
        response = self.client.get(reverse("statuses:delete", kwargs={"pk": self.status.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("statuses:delete", kwargs={"pk": self.status.pk}))
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
