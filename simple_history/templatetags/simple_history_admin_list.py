from django import template
from django.conf import settings
from django.utils import timezone
from django.utils.formats import date_format

register = template.Library()


@register.filter
def display_list_history_date(history_date):
    if getattr(settings, "USE_TZ", False):
        local_time = timezone.localtime(history_date)
        return f"{date_format(local_time, 'DATETIME_FORMAT')} {local_time.tzinfo}"
    return date_format(history_date, "DATETIME_FORMAT")
