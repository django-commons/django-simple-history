from django.apps import AppConfig


class SimpleHistoryConfig(AppConfig):
    name = 'simple_history'
    verbose_name = 'Simple History'

    def ready(self):
        from simple_history.utils import autodiscover_history_modules
        autodiscover_history_modules()
