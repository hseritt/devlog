from django.utils import timezone
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task, Comment
from apps.ui.forms import AddSprintForm


class UIFunctionalTestCase(TestCase):
    def setUp(self):
        admin_user = User.objects.create(username="admin", email="admin@localhost")
        admin_user.set_password("admin")
        admin_user.save()

        nonmember_user = User.objects.create(
            username="testuser1", email="testuser1@localhost"
        )
        nonmember_user.set_password("test")
        nonmember_user.save()

        project = Project.objects.create(name="Example project")
        project.members.add(admin_user)
        project.save()

        sprint = Sprint.objects.create(
            name="Example sprint", leader=admin_user, project=project
        )
        task = Task.objects.create(
            subject="Example task subject", project=project, sprint=sprint
        )
        comment = Comment.objects.create(
            task=task, author=admin_user, content="Example comment"
        )

        client = Client()
        self.client = client
        self.admin_user = admin_user
        self.nonmember_user = nonmember_user
        self.project = project
        self.sprint = sprint
        self.task = task
        self.comment = comment

    def test_add_task_no_sprint(self):
        """DEVL-45"""
        self.client.login(username="admin", password="admin")
        response = self.client.post(
            reverse("ui-add-task-view", args=[self.project.id]),
            {
                "subject": "Sample Subject",
                "type": "Task",
                "status": "New",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.get(subject="Sample Subject", sprint=None))

    def test_add_task_with_sprint(self):
        """DEVL-45"""
        self.client.login(username="admin", password="admin")
        params = {"sprint": self.sprint.id}
        response = self.client.post(
            reverse("ui-add-task-view", args=[self.project.id])
            + "?"  # noqa: W503
            + urlencode(params),  # noqa: W503
            {
                "subject": "Sample Subject with sprint",
                "type": "Task",
                "status": "New",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Task.objects.get(subject="Sample Subject with sprint", sprint=self.sprint)
        )

    def test_add_sprint_with_future(self):
        """DEVL-36"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse("ui-add-sprint-view"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Future" in response.content)

    def test_add_sprint_no_future(self):
        """DEVL-36"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                "ui-update-sprint-view",
                args=[
                    self.sprint.id,
                ],
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(b"Future" in response.content)


class AddSprintViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(name="Test Project", manager=self.user)
        self.project.members.add(self.user)
        self.project.save()
        self.add_sprint_url = reverse("ui-add-sprint-view")

    def test_add_sprint_view_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.add_sprint_url)
        add_sprint_form = response.context["add_sprint_form"]
        self.assertIsInstance(add_sprint_form, AddSprintForm)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ui/add_sprint.html")

    def test_add_sprint_view_post(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "project": self.project.id,
            "name": "Test Sprint",
            "description": "Test Description",
            "leader": self.user.id,
            "status": "Open",
            "started": timezone.now(),
            "end": timezone.now() + timezone.timedelta(days=7),
        }
        self.client.post(self.add_sprint_url, data=data)
        self.assertTrue(Sprint.objects.get(name="Test Sprint"))

    def test_add_sprint_view_get_no_login(self):
        response = self.client.get(self.add_sprint_url)
        self.assertEqual(response.status_code, 302)

    def test_add_sprint_view_post_no_login(self):
        data = {
            "project": self.project.id,
            "name": "Test Sprint",
            "description": "Test Description",
            "leader": self.user.id,
            "status": "Open",
            "started": timezone.now(),
            "end": timezone.now() + timezone.timedelta(days=7),
        }
        response = self.client.post(self.add_sprint_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Sprint.objects.filter(name="Test Sprint"))
