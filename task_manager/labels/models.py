# task_manager/labels/models.py

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Имя"))
    meaning = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Смысл"),
    )
    karma_effect = models.TextField(
        blank=True,
        verbose_name=_("Контекст/Эффект для кармы"),
    )
    created_at = models.DateTimeField(
        verbose_name=_("дата создания"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Метка")
        verbose_name_plural = _("Метки")

    def __str__(self):
        return self.name

    def clean(self):
        if self.pk is None and Label.objects.filter(name=self.name).exists():
            raise ValidationError({"name": _("уже существует")})
