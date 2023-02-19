import logging
from django import template
from django.db.models import Q

from apps.projects.models import Project
from apps.tasks.models import Task


register = template.Library()

CLOSED_QUERY = Q(status="Closed") | Q(status="Won't Fix")
SPRINT_TASK_ORDER = "sprint__started", "effort", "type"


def task_open_status(task_qs):
    try:
        return task_qs.exclude(CLOSED_QUERY).order_by(*SPRINT_TASK_ORDER)
    except Exception as err:
        logging.error(logging.error(f"Error in task_open_status: {err}"))
        return None


def task_finished_status(task_qs):
    try:
        return task_qs.filter(CLOSED_QUERY).order_by(*SPRINT_TASK_ORDER)
    except Exception as err:
        logging.error(logging.error(f"Error in task_finished_status: {err}"))
        return None


def sprint_open_status(sprint_qs):
    try:
        return sprint_qs.filter(status="Open").order_by("-started")
    except Exception as err:
        logging.error(logging.error(f"Error in sprint_open_status: {err}"))
        return None


def sprint_closed_status(sprint_qs):
    try:
        return sprint_qs.filter(status="Ended").order_by("-started")
    except Exception as err:
        logging.error(logging.error(f"Error in sprint_closed_status: {err}"))
        return None


def sprint_future_status(sprint_qs):
    try:
        return sprint_qs.filter(status="Future").order_by("-started")
    except Exception as err:
        logging.error(logging.error(f"Error in sprint_future_status: {err}"))
        return None


def task_backlog(task_qs, project_id):
    try:
        return Task.objects.filter(
            project=Project.objects.get(pk=project_id), sprint=None
        )
    except Exception as err:
        logging.error(logging.error(f"Error in task_backlog: {err}"))
        return None


register.filter("task_open_status", task_open_status)
register.filter("task_finished_status", task_finished_status)
register.filter("sprint_open_status", sprint_open_status)
register.filter("sprint_closed_status", sprint_closed_status)
register.filter("sprint_future_status", sprint_future_status)
register.filter("task_backlog", task_backlog)
