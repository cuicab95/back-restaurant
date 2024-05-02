from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.settings import api_settings


class ConfigAPITest(APITestCase):
    def create_user(
        self,
        username="root",
        password="test",
        **kwargs,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            **kwargs
        )
        return user

    def update_token(self, token):
        auth = f"{api_settings.AUTH_HEADER_TYPES[0]} {token}"
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def authenticate(self, user, password=None):
        password = password or "test"
        user = user.username if isinstance(user, User) else user
        response = self.client.post(
            "/security/api/token/", {"username": user, "password": password}
        )
        if response.status_code == 200:
            self.update_token(response.json().get("access"))
        return response

