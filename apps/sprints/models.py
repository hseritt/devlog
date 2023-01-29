from django.contrib.auth.models import User
from django.db import models

from apps.projects.models import Project


class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    started = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=(("Open", "Open"), ("Ended", "Ended")), default="Open"
    )

    def __str__(self):
        return f"{self.id}:{self.name} {self.started} - {self.end}"
