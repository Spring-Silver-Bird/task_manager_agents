# task_manager/labels/urls.py

from django.urls import path

from task_manager.labels import views

urlpatterns = [
    path("", views.LabelListView.as_view(), name="list"),
    path("create/", views.LabelCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.LabelUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.LabelDeleteView.as_view(), name="delete"),
]
