# task_manager/statuses/models.py

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Имя"))
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
