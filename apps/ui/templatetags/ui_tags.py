from django import template
from django.db.models import Q


register = template.Library()


def task_open_status(task_qs):
    return task_qs.exclude(Q(status="Closed") | Q(status="Won't Fix")).order_by(
        "sprint__started",
        "effort",
        "type",
    )


register.filter("task_open_status", task_open_status)
