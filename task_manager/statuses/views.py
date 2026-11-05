# task_manager/statuses/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/list.html"
    context_object_name = "statuses"

    def handle_no_permission(self):
        messages.error(self.request, "Кто ты, воин? Назови свое имя и станут видны тебе знаки отличия!")
        return super().handle_no_permission()


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно изменен"


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно удален"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.object, "task_set") and self.object.task_set.exists():
            messages.error(request, "Невозможно удалить статус, так как он используется")
            return redirect("statuses:list")
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Невозможно удалить статус, так как он используется")
            return redirect("statuses:list")
