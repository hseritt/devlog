from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.utils import IntegrityError
from django.forms import ValidationError
from django.utils.translation import gettext as _
from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.utils import get_task_title


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        try:
            super(Category, self).save(*args, **kwargs)
        except IntegrityError as err:
            raise ValidationError(
                _(
                    f'Categories are saved with lowercase(). A category with this name ("{self.name}") already exists.'
                )
            )


class Task(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
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
            ("Closed", "Closed"),
            ("Won't Fix", "Won't Fix"),
        ),
        default="New",
    )

    effort = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)], default=5
    )

    type = models.CharField(
        max_length=30,
        choices=(
            ("Task", "Task"),
            ("Feature", "Feature"),
            ("Bug", "Bug"),
            ("Story", "Story"),
            ("Epic", "Epic"),
            ("Spike", "Spike"),
        ),
        default="Task",
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )

    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, null=True, blank=True)

    blocked_by_tasks = models.ManyToManyField("self", blank=True)
    cloned_by_tasks = models.ManyToManyField("self", blank=True)
    related_to_tasks = models.ManyToManyField("self", blank=True)
    blocking_tasks = models.ManyToManyField("self", blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return get_task_title(self)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.task.id} / {self.id}"
