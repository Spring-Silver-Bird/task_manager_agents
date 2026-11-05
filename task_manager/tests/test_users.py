from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Sam", last_name="Vimesy", username="Commander", password="SybilRamkin"
        )

    def test_users_list(self):
        response = self.client.get(reverse("users:list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("users", response.context)

    def test_create_get(self):
        response = self.client.get(reverse("users:create"))
        self.assertEqual(response.status_code, 200)

    def test_create_invalid(self):
        response = self.client.post(
            reverse("users:create"),
            {
                "username": "",
                "first_name": "Fred",
                "last_name": "Colon",
                "password1": "Sergeant!",
                "password2": "Sergeant!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertIn("username", response.context["form"].errors)
        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(User.objects.filter(username="").exists())

    def test_update_get_own(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("users:update", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/update.html")
        self.assertContains(response, "Изменить")

    def test_update_post_own(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("users:update", kwargs={"pk": self.user.pk}),
            {
                "first_name": "Samuel",
                "last_name": "Vimes",
                "username": "Commander",
                "password1": "SybilRamkin1",
                "password2": "SybilRamkin1",
            },
            follow=False,
        )
        self.assertRedirects(response, reverse("users:list"))  # views.py:37
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Samuel")
        self.assertEqual(self.user.last_name, "Vimes")
        self.assertTrue(self.user.check_password("SybilRamkin1"))
        list_resp = self.client.get(reverse("users:list"))
        self.assertContains(list_resp, "Samuel")

    def test_update_forbidden_other(self):
        other = User.objects.create_user(username="Lu-Tze", password="Sweeper1")
        self.client.force_login(other)
        response = self.client.get(reverse("users:update", kwargs={"pk": self.user.pk}))
        self.assertRedirects(response, reverse("users:list"))
        response = self.client.post(
            reverse("users:update", kwargs={"pk": self.user.pk}),
            {"first_name": "Hack", "last_name": "Hack", "username": "Commander"},
        )
        self.assertRedirects(response, reverse("users:list"))
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, "Hack")

    def test_delete_get_own(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("users:delete", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/delete.html")
        self.assertContains(response, "Да, удалить")

    def test_delete_post_own(self):
        self.client.force_login(self.user)
        pk = self.user.pk
        response = self.client.post(reverse("users:delete", kwargs={"pk": pk}))
        self.assertRedirects(response, reverse("users:list"))
        self.assertFalse(User.objects.filter(pk=pk).exists())
        self.assertEqual(User.objects.count(), 0)

    def test_delete_forbidden_other(self):
        other = User.objects.create_user(username="other2", password="pass12345")
        self.client.force_login(other)
        response = self.client.get(reverse("users:delete", kwargs={"pk": self.user.pk}))
        self.assertRedirects(response, reverse("users:list"))
        response = self.client.post(reverse("users:delete", kwargs={"pk": self.user.pk}))
        self.assertRedirects(response, reverse("users:list"))
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_delete_anon(self):
        response = self.client.get(reverse("users:delete", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:list"))
