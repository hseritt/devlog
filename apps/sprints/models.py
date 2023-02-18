from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Sum
from django.apps import apps
from django.utils import timezone


from markdownx.models import MarkdownxField

from apps.projects.models import Project


class Sprint(models.Model):
    """
    A model representing a sprint for a project.
    """

    def default_sprint_name():
        """
        Generate a default name for the sprint based on the current date.

        Returns:
            A string representing the default name for the sprint.
        """
        today = date.today()
        next_week = today + timedelta(days=7)
        return (
            f"Sprint {today.strftime('%Y-%m-%d')} to {next_week.strftime('%Y-%m-%d')}"
        )

    def default_sprint_started():
        """
        Get the default start time for the sprint.

        Returns:
            A datetime representing the default start time for the sprint.
        """
        return timezone.now()

    def default_sprint_end():
        """
        Get the default end time for the sprint.

        Returns:
            A datetime representing the default end time for the sprint.
        """
        return timezone.now() + timezone.timedelta(days=7)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = MarkdownxField(default="", null=True, blank=True)
    name = models.CharField(max_length=50, default=default_sprint_name)
    started = models.DateTimeField(
        default=default_sprint_started, null=True, blank=True
    )
    end = models.DateTimeField(default=default_sprint_end, null=True, blank=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=(
            ("Open", "Open"),
            ("Ended", "Ended"),
            ("Future", "Future"),
        ),
        default="Open",
    )

    def get_velocity(self):
        """
        Get the total effort of all tasks in the sprint.

        Returns:
            An integer representing the total effort of all tasks in the sprint.
        """
        Task = apps.get_model("tasks", "Task")
        return Task.objects.filter(sprint=self).aggregate(Sum("effort"))["effort__sum"]

    def get_total_tasks(self):
        Task = apps.get_model("tasks", "Task")
        return Task.objects.filter(sprint=self).count()

    def get_closed_tasks(self):
        Task = apps.get_model("tasks", "Task")
        return Task.objects.filter(
            Q(status="Closed") | Q(status="Won't Fix"), sprint=self
        )

    def get_closed_tasks_velocity(self):
        Task = apps.get_model("tasks", "Task")
        return Task.objects.filter(
            Q(status="Closed") | Q(status="Won't Fix"), sprint=self
        ).aggregate(Sum("effort"))["effort__sum"]

    def get_completion_pct(self):
        """
        Get the completion percentage of the sprint.

        Returns:
            A float representing the completion percentage of the sprint.
        """
        Task = apps.get_model("tasks", "Task")
        try:
            return float(len(self.get_closed_tasks())) / float(self.get_total_tasks())
        except ZeroDivisionError:
            return 0

    def get_progress(self):
        Task = apps.get_model("tasks", "Task")
        try:
            return float(self.get_closed_tasks_velocity()) / float(self.get_velocity())
        except ZeroDivisionError:
            return 0
        except TypeError:
            return None

    def __str__(self):
        """
        Return a string representation of the sprint.

        Returns:
            A string representing the sprint's name.
        """
        return f"{self.name}"
