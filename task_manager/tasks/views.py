# task_manager/tasks/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"

    def handle_no_permission(self):
        messages.error(self.request, "Кто ты, воин? Назови свое имя и узришь множество тайн!")
        return super().handle_no_permission()

    def get_queryset(self):
        return TaskFilter(self.request.GET, queryset=Task.objects.all(), request=self.request).qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter"] = TaskFilter(self.request.GET, queryset=Task.objects.all(), request=self.request)
        return ctx


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно изменена"


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно удалена"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks:list")


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
