from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.core.lib.system import get_system_user


class AuthTestCase(TestCase):
    def test_get_system_user(self):
        User = get_user_model()
        system_user = User.objects.create_user(username="system")
        admin_user = User.objects.create_user(username="admin")

        # Test when the 'system' user exists
        result = get_system_user()
        self.assertEqual(result, system_user)

        # Test when the 'system' user doesn't exist but the 'admin' user does
        system_user.delete()
        result = get_system_user()
        self.assertEqual(result, admin_user)

        # Test when neither 'system' nor 'admin' users exist
        admin_user.delete()
        with self.assertRaises(User.DoesNotExist):
            get_system_user()
