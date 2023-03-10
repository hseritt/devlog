from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.utils import IntegrityError
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

from markdownx.models import MarkdownxField
from apps.core.lib.system import get_system_user

from apps.sprints.models import Sprint
from apps.tasks.utils import get_task_title
from apps.projects.models import Project


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return (
            f"{self.project.name} / {self.name}"
            if self.project
            else f"General / {self.name}"
        )

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError(
                _(
                    f"A category with name '{self.name}' already exists. Please choose a different name."
                )
            )


class Task(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    description = MarkdownxField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="task_assigned_to",
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date_closed = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=30,
        choices=(
            ("New", "New"),
            ("Investigation", "Investigation"),
            ("In Progress", "In Progress"),
            ("Awaiting Review", "Awaiting Review"),
            ("In Review", "In Review"),
            ("Awaiting Deployment", "Awaiting Deployment"),
            ("Closed", "Closed"),
            ("Won't Fix", "Won't Fix"),
        ),
        default="New",
    )

    last_action_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="task_last_action_by",
    )

    effort = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        default=5,
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=30,
        choices=(
            ("Bug", "Bug"),
            ("Feature", "Feature"),
            ("Enhancement", "Enhancement"),
            ("Epic", "Epic"),
            ("Spike", "Spike"),
            ("Story", "Story"),
            ("Task", "Task"),
        ),
        default="Task",
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )

    sprint = models.ForeignKey(
        Sprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )

    blocked_by_tasks = models.ManyToManyField("self", blank=True)
    cloned_by_tasks = models.ManyToManyField("self", blank=True)
    related_to_tasks = models.ManyToManyField("self", blank=True)
    blocking_tasks = models.ManyToManyField("self", blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return get_task_title(self)

    def save(self, *args, **kwargs):
        if self.pk:
            # retrieve the old status from the database
            old_task = Task.objects.get(pk=self.pk)
            old_status = old_task.status
            new_status = self.status

            # check if the status has changed
            if old_status != new_status:
                system_user = get_system_user()
                if system_user:
                    content = f"Task status changed from {old_status} to {new_status} by {self.last_action_by}"
                    Comment.objects.create(
                        task=self,
                        author=system_user,
                        content=content,
                    )

        self.date_closed = (
            timezone.now() if self.status in ("Closed", "Won't Fix") else None
        )
        super().save(*args, **kwargs)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.task.id} / {self.id}"
