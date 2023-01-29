from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.projects.models import Project


class Task(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default="admin"
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=30,
        choices=(
            ("New", "New"),
            ("Investigation", "Investigation"),
            ("In Progress", "In Progress"),
            ("Awaiting Review", "Awaiting Review"),
            ("In Review", "In Review"),
            ("Awaiting Deployment", "Awaiting Deployment"),
            ("Deployed", "Deployed"),
            ("Closed", "Closed"),
        ),
        default="New",
    )

    effort = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)], default=5
    )

    type = models.CharField(
        max_length=30,
        choices=(
            ("Feature", "Feature"),
            ("Bug", "Bug"),
            ("Task", "Task"),
            ("Sub Task", "Sub Task"),
        ),
        default="Task",
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        try:
            title = f"{self.project.prefix}-{self.id} / {self.subject} / {self.status}"
        except AttributeError as err:
            if (
                repr(err)
                == "AttributeError(\"'NoneType' object has no attribute 'prefix'\")"  # noqa: W503
            ):
                title = f"{self.id} / {self.subject} / {self.status}"
        return title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task.id} / {self.id}"
