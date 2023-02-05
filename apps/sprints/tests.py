from django.test import TestCase
from apps.projects.models import Project
from apps.sprints.models import Sprint
from django.contrib.auth.models import User
from apps.tasks.models import Task


class SprintVelocityTestCase(TestCase):
    """DEVL-28"""

    def setUp(self):
        User.objects.create(username="admin", email="admin@localhost")
        Project.objects.create(
            name="Example Project",
            prefix="EP",
            description="Example project description",
            manager=User.objects.get(username="admin"),
        )
        sprint = Sprint.objects.create(
            name="Sprint 1",
            project=Project.objects.get(name="Example Project"),
            leader=User.objects.get(username="admin"),
        )
        for i in range(5):
            Task.objects.create(
                subject=f"Issue number {i}",
                description="Example description",
                effort=5,
                sprint=sprint,
            )

    def test_velocity(self):
        sprint = Sprint.objects.get(name="Sprint 1")
        self.assertEqual(sprint.get_velocity(), 25)

    def test_completion_pct(self):
        sprint = Sprint.objects.get(name="Sprint 1")
        task = Task.objects.get(subject="Issue number 1")
        task.status = "Closed"
        task.save()

        self.assertEqual(sprint.get_completion_pct(), 0.2)
