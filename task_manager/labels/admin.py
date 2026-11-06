from django.contrib import admin

from task_manager.labels.models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "meaning", "karma_effect", "created_at")
    search_fields = ("name", "meaning", "karma_effect")
