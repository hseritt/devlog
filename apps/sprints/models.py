from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Sum
from django.apps import apps

from markdownx.models import MarkdownxField

from apps.projects.models import Project


class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = MarkdownxField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    started = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=(
            ("Open", "Open"),
            ("Ended", "Ended"),
            ("Not Started", "Not Started/Future"),
        ),
        default="Open",
    )

    def get_velocity(self):
        Task = apps.get_model("tasks", "Task")
        return Task.objects.filter(sprint=self).aggregate(Sum("effort"))["effort__sum"]

    def get_completion_pct(self):
        Task = apps.get_model("tasks", "Task")
        try:
            return float(
                len(
                    Task.objects.filter(
                        Q(status="Closed") | Q(status="Won't Fix"), sprint=self
                    )
                )
            ) / float(Task.objects.filter(sprint=self).count())
        except ZeroDivisionError:
            return 0

    def __str__(self):
        return f"{self.name}"
