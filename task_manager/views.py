# task_manager/views.py

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView

User = get_user_model()


class IndexView(TemplateView):
    template_name = "index.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = "Вы залогинены"


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def server_error(request):
    return render(request, "500.html", status=500)
