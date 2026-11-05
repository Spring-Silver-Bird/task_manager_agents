# task_manager/users/views.py

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import RegisterForm, UpdateForm

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно изменен"

    def test_func(self):
        return self.request.user.pk == self.kwargs["pk"]

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect("users:list")


class UserDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.authored_tasks.exists() or self.object.executed_tasks.exists():
            messages.error(request, "Вы не можете покинуть нас, так как еще остались задачи")
            return redirect("users:list")
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Вы не можете покинуть нас, так как еще остались задачи")
            return redirect("users:list")

    success_url = reverse_lazy("users:list")
    success_message = "Пользователь успешно удален"

    def test_func(self):
        return self.request.user.pk == self.kwargs["pk"]

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect("users:list")
