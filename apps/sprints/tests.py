from django.test import TestCase, Client
from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task

from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404, HttpResponseNotFound
from unittest.mock import patch
from apps.ui.forms import AddSprintForm
from apps.ui.views import AddSprintView


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

    def test_progress(self):
        sprint = Sprint.objects.get(name="Sprint 1")
        task = Task.objects.get(subject="Issue number 1")
        task.status = "Closed"
        task.save()

        task = Task.objects.get(subject="Issue number 2")
        task.status = "Closed"
        task.save()

        self.assertEqual(sprint.get_progress(), 0.4)


class AddSprintViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpass"
        )

    def test_get_no_projects(self):
        url = reverse("ui-add-sprint-view")
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(url)
        self.assertTrue(b"Not Found" in response.content)

    def test_post_no_projects(self):
        url = reverse("ui-add-sprint-view")
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(url)
        self.assertTrue(b"Not Found" in response.content)

    def test_get_projects(self):
        project = Project.objects.create(name="Test Project")
        project.members.add(self.user)
        project.save()
        url = reverse("ui-add-sprint-view")
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_valid_form(self):
        project = Project.objects.create(name="Test Project")
        project.members.add(self.user)
        project.save()
        url = reverse("ui-add-sprint-view")
        self.client.force_login(self.user)
        data = {"name": "Test Sprint", "project": project.id, "leader": self.user.id}
        self.client.post(url, data)
        with self.assertRaises(Sprint.DoesNotExist):
            Sprint.objects.get(name="Test Sprint")

    def test_post_invalid_form(self):
        project = Project.objects.create(name="Test Project")
        project.members.add(self.user)
        project.save()
        url = reverse("ui-add-sprint-view")
        self.client.force_login(self.user)
        data = {"name": "", "project": project.id, "leader": self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
