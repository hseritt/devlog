from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task, Comment


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
