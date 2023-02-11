from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase, Client
from psycopg2.errors import UniqueViolation
from django.core.exceptions import ValidationError

from apps.projects.models import Project
from apps.sprints.models import Sprint

from .models import Category, Comment, Task


class CategoryCaseInsensitiveUniqueTestCase(TestCase):
    """DEVL-31"""

    def setUp(self):
        Category.objects.create(name="Network")

    def test_integrity_error(self):
        with self.assertRaises(ValidationError):
            Category.objects.create(name="NETWORK")
            Category.objects.create(name="network")
            Category.objects.create(name="Network")


class DateClosedTestCase(TestCase):
    """DEVL-48"""

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

    def test_date_closed_field(self):
        task = Task.objects.get(subject="Example task subject")
        self.assertTrue(hasattr(task, "date_closed"))

    def test_date_closed_on_close(self):
        task = Task.objects.get(subject="Example task subject")
        task.status = "Closed"
        task.save()
        self.assertIsNotNone(task.date_closed)

    def test_date_closed_on_wontfix(self):
        task = Task.objects.get(subject="Example task subject")
        task.status = "Won't Fix"
        task.save()
        self.assertIsNotNone(task.date_closed)

    def test_date_closed_on_opened(self):
        task = Task.objects.get(subject="Example task subject")
        for status in (
            "In Progress",
            "New",
            "Investigation",
            "Awaiting Review",
            "In Review",
            "Awaiting Deployment",
        ):
            task.status = status
            task.save()
            self.assertIsNone(task.date_closed)

            task.status = "Closed"
            task.save()
            self.assertIsNotNone(task.date_closed)
