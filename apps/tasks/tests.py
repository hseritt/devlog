from django.db.utils import IntegrityError
from django.test import TestCase
from psycopg2.errors import UniqueViolation
from django.core.exceptions import ValidationError

from .models import Category


class CategoryCaseInsensitiveUniqueTestCase(TestCase):
    """DEVL-31"""

    def setUp(self):
        Category.objects.create(name="Network")

    def test_integrity_error(self):
        with self.assertRaises(ValidationError):
            Category.objects.create(name="NETWORK")
            Category.objects.create(name="network")
            Category.objects.create(name="Network")
