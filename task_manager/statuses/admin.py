from django.contrib import admin

from task_manager.statuses.models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status_type", "when_to_apply", "created_at")
    list_filter = ("status_type",)
    search_fields = ("name", "when_to_apply")
