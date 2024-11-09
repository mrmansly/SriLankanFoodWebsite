from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient


def get_authenticated_user() -> User:
    return User.objects.create(username='testuser', password='testpassword')


def get_authenticated_client(authenticated=True) -> APIClient:
    client = APIClient()
    client.force_authenticate(get_authenticated_user() if authenticated else None)
    return client


def get_access_token() -> str:
    user = get_authenticated_user()
    refresh = RefreshToken.for_user(user)
    return str(refresh.token)
