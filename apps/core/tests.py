from django.contrib.auth.models import User
from django.test import TestCase

from apps.projects.models import Project


class BaseTestCase(TestCase):
    def setUp(self):
        ...

    def test_base(self):
        self.assertTrue(True)
