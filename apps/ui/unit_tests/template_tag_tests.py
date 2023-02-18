from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task
from apps.ui.templatetags.ui_tags import (
    sprint_closed_status,
    sprint_future_status,
    sprint_open_status,
    task_backlog,
    task_finished_status,
    task_open_status,
)


class TemplateTagsTestCase(TestCase):
    def setUp(self):
        admin_user = User.objects.create(username="admin", email="admin@localhost")
        admin_user.set_password("admin")
        admin_user.save()

        nonmember_user = User.objects.create(
            username="testuser1", email="testuser1@localhost"
        )
        nonmember_user.set_password("test")
        nonmember_user.save()

        self.project = Project.objects.create(name="Test Project")
        self.sprint1 = Sprint.objects.create(
            name="Sprint 1",
            project=self.project,
            status="Open",
            started=timezone.now(),
            leader=admin_user,
        )
        self.sprint2 = Sprint.objects.create(
            name="Sprint 2",
            project=self.project,
            status="Ended",
            started=timezone.now(),
            leader=admin_user,
        )
        self.task1 = Task.objects.create(
            subject="Task 1",
            project=self.project,
            sprint=self.sprint1,
            status="In Progress",
        )
        self.task2 = Task.objects.create(
            subject="Task 2",
            project=self.project,
            sprint=self.sprint2,
            status="Closed",
        )
        self.admin_user = admin_user

    def test_task_open_status(self):
        qs = Task.objects.all()
        result = task_open_status(qs)
        if result:
            for row in result:
                self.assertTrue(row.status == "Open" or row.status == "In Progress")

    def test_task_finished_status(self):
        qs = Task.objects.all()
        result = task_finished_status(qs)
        if result:
            for row in result:
                self.assertTrue(row.status == "Closed" or row.status == "Won't Fix")

    def test_sprint_open_status(self):
        qs = Sprint.objects.all()
        result = sprint_open_status(qs)
        if result:
            for row in result:
                self.assertTrue(row.status != "Closed" or row.status != "Won't Fix")

    def test_sprint_closed_status(self):
        qs = Sprint.objects.all()
        result = sprint_closed_status(qs)
        if result:
            for row in result:
                self.assertTrue(row.status == "Ended")

    def test_sprint_future_status(self):
        Sprint.objects.create(
            name="Future Sprint",
            project=self.project,
            status="Future",
            started=timezone.now(),
            leader=self.admin_user,
        )
        qs = Sprint.objects.all()
        result = sprint_future_status(qs)
        if result:
            for row in result:
                self.assertTrue(row.status == "Future")

    def test_task_backlog(self):
        Task.objects.create(subject="Backlog Task", project=self.project)
        qs = Task.objects.all()
        result = task_backlog(qs, self.project.pk)
        if result:
            for row in result:
                self.assertIsNone(row.sprint)
