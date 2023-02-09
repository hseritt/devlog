from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task, Comment


class UIUrlsBaseTestCase(TestCase):
    def setUp(self):
        admin_user = User.objects.create(username="admin", email="admin@localhost")
        admin_user.set_password("admin")
        admin_user.save()

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
        self.project = project
        self.sprint = sprint
        self.task = task
        self.comment = comment

    def test_index_view(self):
        url = "ui-index-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse(url))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(reverse(url), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)

    def test_project_view(self):
        url = "ui-project-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.project.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.project.id,
                ],
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)

    def test_sprint_view(self):
        url = "ui-sprint-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.sprint.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.sprint.id,
                ],
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)

    def test_task_view(self):
        url = "ui-task-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.task.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.task.id,
                ],
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)

    def test_add_task_view(self):
        url = "ui-add-task-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.project.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.task.id,
                ],
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)

    def test_update_task_view(self):
        url = "ui-update-task-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.task.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.task.id,
                ],
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)

    def test_add_comment_view(self):
        url = "ui-add-comment-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.task.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.task.id,
                ],
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)

    def test_update_sprint_view(self):
        url = "ui-update-sprint-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.sprint.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(
            reverse(
                url,
                args=[
                    self.sprint.id,
                ],
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)

    def test_add_sprint_view(self):
        url = "ui-add-sprint-view"
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse(
                url,
            )
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(
            reverse(
                url,
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"/auth/login" in response.content)
