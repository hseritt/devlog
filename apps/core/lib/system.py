from django.contrib.auth import get_user_model


def get_system_user():
    User = get_user_model()
    try:
        return User.objects.get(username="system")
    except User.DoesNotExist:
        return User.objects.get(username="admin")
