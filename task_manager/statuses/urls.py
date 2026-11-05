# task_manager/statuses/urls.py

from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path("", views.StatusListView.as_view(), name="list"),
    path("create/", views.StatusCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.StatusUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.StatusDeleteView.as_view(), name="delete"),
]
