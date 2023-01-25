from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
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

    def __str__(self):
        return self.name
