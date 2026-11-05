# task_manager/labels/views.py

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

from task_manager.labels.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/list.html"
    context_object_name = "labels"

    def handle_no_permission(self):
        messages.error(self.request, "Кто ты, воин? Назови свое имя и откроются тебе тайные знаки!")
        return super().handle_no_permission()


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ["name"]
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно изменена"


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно удалена"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(request, "Невозможно удалить метку, так как она используется")
            return redirect("labels:list")
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Невозможно удалить метку, так как она используется")
            return redirect("labels:list")
