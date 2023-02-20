from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    prefix = models.CharField(max_length=4, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    scope = models.CharField(
        max_length=30,
        choices=(
            ("Sandbox", "Sandbox"),
            ("R&D", "R&D"),
            ("Internal", "Internal"),
            ("Public Product", "Public Product"),
            ("Private Product", "Private Product"),
        ),
        default="R&D",
    )
    members = models.ManyToManyField(User, blank=True, related_name="projects")
    manager = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="managed_projects",
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        prefix_str = f" / {self.prefix}" if self.prefix else ""
        return f"{self.id} / {self.name}{prefix_str}"
