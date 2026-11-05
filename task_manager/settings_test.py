from task_manager.settings import *  # noqa: F403
from task_manager.settings import STORAGES as BASE_STORAGES

STORAGES = {
    **BASE_STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
