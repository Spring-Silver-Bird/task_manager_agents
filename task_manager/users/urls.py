# task_manager/users/urls.py

from django.urls import path

from task_manager.users import views

urlpatterns = [
    path("create/", views.UserCreateView.as_view(), name="create"),
    path("", views.UserListView.as_view(), name="list"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete"),
]
