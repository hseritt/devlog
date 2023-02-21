import datetime
from django.utils import timezone
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task, Comment, Category
from apps.ui.forms import AddSprintForm
from apps.ui.forms import AddCategoryForm
from apps.ui.views import AddCategoryView


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


class AddCategoryViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.project = Project.objects.create(
            name="Test Project",
            prefix="TP",
            description="Test project description",
            manager=self.user,
        )
        self.add_category_url = reverse("ui-add-category-view", args=[self.project.id])
        self.add_category_form_data = {
            "name": "Test Category",
            "description": "Test category description",
        }

    def test_get(self):
        request = self.factory.get(self.add_category_url)
        request.user = self.user
        response = AddCategoryView.as_view()(request, project_id=self.project.id)
        self.assertEqual(response.status_code, 200)

    def test_post_success(self):
        request = self.factory.post(
            self.add_category_url, data=self.add_category_form_data
        )
        request.user = self.user
        response = AddCategoryView.as_view()(request, project_id=self.project.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse("ui-add-task-view", args=[self.project.id])
        )
        self.assertEqual(Category.objects.count(), 1)
        category = Category.objects.first()
        self.assertEqual(category.name, self.add_category_form_data["name"])
        self.assertEqual(
            category.description, self.add_category_form_data["description"]
        )
        self.assertEqual(category.project, self.project)

    def test_post_failure(self):
        add_category_form_data = {"name": ""}
        request = self.factory.post(self.add_category_url, data=add_category_form_data)
        request.user = self.user
        response = AddCategoryView.as_view()(request, project_id=self.project.id)

        self.assertEqual(response.status_code, 200)


class AddSprintViewTestStatus(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(name="Test Project", manager=self.user)
        self.project.members.add(self.user)
        self.project.save()
        self.client = Client()

    def test_add_sprint_form(self):
        # Create an open sprint
        self.client.login(username="testuser", password="testpass")
        Sprint.objects.create(
            name="Open Sprint", leader=self.user, status="Open", project=self.project
        )

        # Call the AddSprintView with the test user
        response = self.client.get(
            reverse("ui-add-sprint-view"), {"user": self.user.id}
        )

        # Check that the response contains the Future option in the status field
        self.assertContains(response, '<option value="Future">Future</option>')

        # Check that the response contains the help text for the status field
        # print(response.content)
        # self.assertContains(
        #     response,
        #     "No open sprints can be created if there are any sprints currently open.",
        # )

        # Check that the response contains the form submission button
        self.assertTrue(b"Submit" in response.content)

    def test_add_sprint_form_no_open_sprints(self):
        # Call the AddSprintView with the test user
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("ui-add-sprint-view"), {"user": self.user.id}
        )

        # Check that the response does contain the Open option in the status field
        self.assertTrue(b"Open" in response.content)

        # Check that the response does not contain the help text for the status field
        self.assertNotContains(
            response,
            "No open sprints can be created if there are any sprints currently open.",
        )

        # Check that the response contains the form submission button
        self.assertTrue(b"Submit" in response.content)


class TaskDetailPageTestCase(TestCase):
    def setUp(self):
        # create a user to assign the task to
        admin_user = User.objects.create(username="admin", email="admin@localhost")
        admin_user.set_password("admin")
        admin_user.save()
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # create a project and a sprint for the task
        self.project = Project.objects.create(
            name="Test Project",
            prefix="TP",
            description="Test project description",
            manager=self.user,
        )
        self.sprint = Sprint.objects.create(
            name="Test Sprint",
            project=self.project,
            leader=self.user,
        )

        # create a task to test
        self.task = Task.objects.create(
            subject="Test Task",
            assigned_to=self.user,
            project=self.project,
            sprint=self.sprint,
        )
        self.comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content="This is a comment\nwith a linebreak",
        )

    def test_task_detail_page_linebreaks(self):
        response = self.client.get(reverse("ui-task-detail-view", args=[self.task.id]))
        self.assertContains(response, "This is a comment<br>\nwith a linebreak")
