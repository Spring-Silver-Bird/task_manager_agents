# task_manager/tests/test_tasks.py

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class FiltersTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="tester1", password="pass1234")
        self.user2 = User.objects.create_user(username="tester2", password="1234pass")
        self.status1 = Status.objects.create(name="new")
        self.status2 = Status.objects.create(name="done")
        self.labels1 = Label.objects.create(name="FirstLabel")
        self.labels2 = Label.objects.create(name="SecondLabel")
        self.task1 = Task.objects.create(
            name="First_task",
            description="some description",
            status=self.status1,
            author=self.user1,
            executor=self.user2,
        )
        self.task2 = Task.objects.create(
            name="Second_task",
            description="other description",
            status=self.status2,
            author=self.user2,
            executor=self.user1,
        )
        self.task3 = Task.objects.create(
            name="Third_task",
            description="some description",
            status=self.status1,
            author=self.user1,
            executor=self.user1,
        )
        self.task4 = Task.objects.create(
            name="Force_task",
            description="other description",
            status=self.status2,
            author=self.user2,
            executor=self.user2,
        )
        self.task1.labels.set([self.labels2])
        self.task2.labels.set([self.labels1])
        self.task3.labels.set([self.labels1])
        self.task4.labels.set([self.labels2])

    def test_filter_form(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("filter", response.context)
        flt = response.context["filter"]
        for name in ("status", "executor", "labels", "self_tasks"):
            self.assertIn(name, flt.form.fields)
        self.assertContains(response, "Статус:")
        self.assertContains(response, "Исполнитель:")
        self.assertContains(response, "Метка:")
        self.assertContains(response, "Только свои задачи")
        self.assertContains(response, "Показать")
        self.assertContains(response, 'name="status"')
        self.assertContains(response, 'name="executor"')
        self.assertContains(response, 'name="labels"')
        self.assertContains(response, 'name="self_tasks"')
        self.assertContains(response, 'type="checkbox"')
        self.assertContains(response, "<select")

    def test_filter_by_status(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("tasks:list"), {"status": self.status1.pk})
        self.assertEqual(response.status_code, 200)
        tasks = list(response.context["tasks"])
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task3, tasks)
        self.assertNotIn(self.task2, tasks)
        self.assertNotIn(self.task4, tasks)
        self.assertContains(response, "First_task")
        self.assertContains(response, "Third_task")
        self.assertNotContains(response, "Second_task")

    def test_filter_by_executor(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("tasks:list"), {"executor": self.user1.pk})
        self.assertEqual(response.status_code, 200)
        tasks = list(response.context["tasks"])
        self.assertIn(self.task2, tasks)
        self.assertIn(self.task3, tasks)
        self.assertNotIn(self.task1, tasks)
        self.assertNotIn(self.task4, tasks)
        self.assertContains(response, "Second_task")
        self.assertContains(response, "Third_task")
        self.assertNotContains(response, "First_task")

    def test_filter_by_label(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("tasks:list"), {"labels": self.labels1.pk})
        self.assertEqual(response.status_code, 200)
        tasks = list(response.context["tasks"])
        self.assertIn(self.task2, tasks)
        self.assertIn(self.task3, tasks)
        self.assertNotIn(self.task1, tasks)
        self.assertNotIn(self.task4, tasks)
        self.assertContains(response, "Second_task")
        self.assertContains(response, "Third_task")
        self.assertNotContains(response, "First_task")

    def test_filter_self_tasks(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(len(list(response.context["tasks"])), 4)
        response = self.client.get(reverse("tasks:list"), {"self_tasks": "on"})
        self.assertEqual(response.status_code, 200)
        tasks = list(response.context["tasks"])
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task3, tasks)
        self.assertNotIn(self.task2, tasks)
        self.assertNotIn(self.task4, tasks)
        self.assertContains(response, "First_task")
        self.assertNotContains(response, "Second_task")
