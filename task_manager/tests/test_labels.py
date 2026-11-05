# task_manager/tests/test_labels.py

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class LabelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.labels = Label.objects.create(name="Test")

    def test_list_guest(self):
        response = self.client.get(reverse("labels:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_create_get_guest(self):
        response = self.client.get(reverse("labels:create"))
        self.assertEqual(response.status_code, 302)

    def test_create_post_guest(self):
        count_before = Label.objects.count()
        response = self.client.post(reverse("labels:create"), {"name": "New"})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertEqual(Label.objects.count(), count_before)

    def test_update_get_guest(self):
        response = self.client.get(reverse("labels:update", kwargs={"pk": self.labels.pk}))
        self.assertEqual(response.status_code, 302)

    def test_update_post_guest(self):
        response = self.client.post(reverse("labels:update", kwargs={"pk": self.labels.pk}), {"name": "Hack"})
        self.assertEqual(response.status_code, 302)
        self.labels.refresh_from_db()
        self.assertNotEqual(self.labels.name, "Hack")

    def test_delete_get_guest(self):
        response = self.client.get(reverse("labels:delete", kwargs={"pk": self.labels.pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_post_guest(self):
        pk = self.labels.pk
        response = self.client.post(reverse("labels:delete", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=pk).exists())

    def test_status_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels:list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("labels", response.context)

    def test_create_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels:create"))
        self.assertEqual(response.status_code, 200)

    def test_create_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("labels:create"),
            {
                "name": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertIn("name", response.context["form"].errors)
        self.assertEqual(Label.objects.count(), 1)
        self.assertFalse(Label.objects.filter(name="").exists())

    def test_update_get_own(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels:update", kwargs={"pk": self.labels.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/update.html")
        self.assertContains(response, "Изменить")

    def test_update_post_own(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("labels:update", kwargs={"pk": self.labels.pk}), {"name": "black"}, follow=False
        )
        self.assertRedirects(response, reverse("labels:list"))
        self.labels.refresh_from_db()
        self.assertEqual(self.labels.name, "black")
        list_resp = self.client.get(reverse("labels:list"))
        self.assertContains(list_resp, "black")

    def test_update_other_allowed(self):
        other = User.objects.create_user(username="Lu-Tze", password="Sweeper1")
        self.client.force_login(other)
        response = self.client.get(reverse("labels:update", kwargs={"pk": self.labels.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("labels:update", kwargs={"pk": self.labels.pk}), {"name": "Hack"})
        self.assertRedirects(response, reverse("labels:list"))
        self.labels.refresh_from_db()
        self.assertEqual(self.labels.name, "Hack")

    def test_delete_get_own(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels:delete", kwargs={"pk": self.labels.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/delete.html")
        self.assertContains(response, "Да, удалить")

    def test_delete_post_own(self):
        self.client.force_login(self.user)
        pk = self.labels.pk
        response = self.client.post(reverse("labels:delete", kwargs={"pk": pk}))
        self.assertRedirects(response, reverse("labels:list"))
        self.assertFalse(Label.objects.filter(pk=pk).exists())
        self.assertEqual(Label.objects.count(), 0)

    def test_delete_protected(self):
        self.client.force_login(self.user)
        status = Status.objects.create(name="S1")
        task = Task.objects.create(name="T1", description="d", status=status, author=self.user, executor=self.user)
        task.labels.add(self.labels)
        response = self.client.post(reverse("labels:delete", kwargs={"pk": self.labels.pk}), follow=True)
        self.assertRedirects(response, reverse("labels:list"))
        self.assertTrue(Label.objects.filter(pk=self.labels.pk).exists())
        self.assertContains(response, "Невозможно удалить метку")

    def test_delete_other_allowed(self):
        other = User.objects.create_user(username="other2", password="pass12345")
        self.client.force_login(other)
        response = self.client.get(reverse("labels:delete", kwargs={"pk": self.labels.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("labels:delete", kwargs={"pk": self.labels.pk}))
        self.assertRedirects(response, reverse("labels:list"))
        self.assertFalse(Label.objects.filter(pk=self.labels.pk).exists())
