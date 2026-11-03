from django.apps import AppConfig


class SimpleHistoryAppConfig(AppConfig):
    name = "simple_history"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from .models import _process_pending_finalizations

        _process_pending_finalizations()
