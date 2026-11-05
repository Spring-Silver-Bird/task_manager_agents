from django import forms
from django.contrib.auth import get_user_model

from task_manager.tasks.models import Task

User = get_user_model()


def user_full_name(user):
    return user.get_full_name().strip() or user.username


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Исполнитель",
        required=False,
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "labels": "Метки",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].label_from_instance = user_full_name
