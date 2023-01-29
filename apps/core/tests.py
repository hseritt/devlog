from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        pass

    def test_base(self):
        self.assertTrue(True)
