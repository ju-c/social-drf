from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class Login(TestCase):
    @staticmethod
    def get_user_access_token(user, password):
        login_url = reverse("api:authentication:token_obtain_pair")
        credentials = {"email": user, "password": password}
        client = APIClient()
        login_response = client.post(login_url, credentials, format="json")
        access_token = login_response.data.get("access")
        return {"access": access_token}
