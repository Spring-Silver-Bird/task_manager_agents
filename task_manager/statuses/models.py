# task_manager/statuses/models.py

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusType(models.TextChoices):
    BACKLOG = "backlog", _("Backlog")
    TODO = "todo", _("To Do")
    IN_PROGRESS = "in_progress", _("In Progress")
    REVIEW = "review", _("Review")
    BLOCKED = "blocked", _("Blocked")
    DONE = "done", _("Done")


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Имя"))
    when_to_apply = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Когда применять"),
    )
    status_type = models.CharField(
        max_length=20,
        choices=StatusType.choices,
        default=StatusType.BACKLOG,
        verbose_name=_("Тип"),
    )
    created_at = models.DateTimeField(
        verbose_name=_("дата создания"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Статус")
        verbose_name_plural = _("Статусы")

    def __str__(self):
        return self.name

    def clean(self):
        if self.pk is None and Status.objects.filter(name=self.name).exists():
            raise ValidationError({"name": _("уже существует")})
