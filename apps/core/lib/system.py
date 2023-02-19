from django.contrib.auth.models import User


def get_system_user():
    try:
        return User.objects.get(username="system")
    except User.DoesNotExist:
        return User.objects.get(username="admin")
