from django import template
from django.db.models import Q


register = template.Library()

CLOSED_QUERY = Q(status="Closed") | Q(status="Won't Fix")
SPRINT_TASK_ORDER = "sprint__started", "effort", "type"


def task_open_status(task_qs):
    return task_qs.exclude(CLOSED_QUERY).order_by(*SPRINT_TASK_ORDER)


def task_finished_status(task_qs):
    return task_qs.filter(CLOSED_QUERY).order_by(*SPRINT_TASK_ORDER)


def sprint_open_status(sprint_qs):
    return sprint_qs.filter(status="Open").order_by("-started")


register.filter("task_open_status", task_open_status)
register.filter("task_finished_status", task_finished_status)
register.filter("sprint_open_status", sprint_open_status)
