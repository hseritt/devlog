from django.contrib.auth.models import User
from django.db import models


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
    members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        try:
            title = f"{self.name} / {self.prefix}"
        except AttributeError:
            title = f"{self.name}"
        return title
