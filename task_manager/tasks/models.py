# task_manager/tasks/models.py

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Задача"))
    description = models.TextField(verbose_name=_("Описание"), blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="task_set")
    labels = models.ManyToManyField(Label, blank=True, related_name="tasks", verbose_name="Метки")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="authored_tasks")
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="executed_tasks",
        verbose_name="Исполнитель",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("дата создания"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")

    def __str__(self):
        return self.name

    def clean(self):
        if self.pk is None and Task.objects.filter(name=self.name).exists():
            raise ValidationError({"name": _("уже существует")})
