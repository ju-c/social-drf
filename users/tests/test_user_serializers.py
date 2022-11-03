from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils.tests.login import Login


class CreateUserViewTests(TestCase):
    def setUp(self):
        self.new_user = {
            "username": "FakeUser1",
            "email": "fakeuser@test.com",
            "password": "testpass123",
            "confirm_password": "testpass123",
        }
        self.url = reverse("api:user-list")

    def test_creating_user(self):
        """
        status_code returns 201 CREATED status response when a new user
        is properly created.
        """
        response = self.client.post(self.url, self.new_user, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_password_on_creating_user(self):
        """
        status_code returns a 400 BAD REQUEST status response for a user
        whose confirm_password is different than the entered password.
        """
        self.new_user["confirm_password"] = "badpassword"
        response = self.client.post(self.url, self.new_user, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_request_data(self):
        """
        status_code returns a 400 BAD REQUEST status response if a post
        request is done without a proper password.
        """
        del self.new_user["password"]
        response = self.client.post(self.url, self.new_user, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserViewSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_a = get_user_model().objects.create_user(
            email="testuser@test.com", password="testpass123", username="testuser1"
        )
        cls.user_b = get_user_model().objects.create_user(
            email="newtestuser@test.com", password="testpass1234", username="testuser2"
        )

        cls.uuid = cls.user_a.uuid
        cls.follower_uuid = cls.user_b.uuid

    def setUp(self) -> None:
        access_token = Login.get_user_access_token(
            self.user_a.email, "testpass123"
        ).get("access")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_edit_profile(self):
        """
        status_code returns a 200 OK status response when a user profile
        is properly edited.
        """
        new_username = "NewUserName"
        patch_url = reverse("api:user-detail", kwargs={"uuid": self.uuid})
        response = self.client.patch(patch_url, {"username": new_username})
        updated_user = get_user_model().objects.get(uuid=self.uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.username, new_username)

    def test_follow_user(self):
        """
        status_code returns a 200 OK status response when a user follows
        another user.
        """
        requested_data = {"action": "FOLLOW", "follow_uuid": self.follower_uuid}
        patch_url = reverse("api:user-detail", kwargs={"uuid": self.uuid})
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        followed_user = get_user_model().objects.get(uuid=self.follower_uuid)
        self.assertEqual(followed_user.followers.count(), 1)

    def test_following_a_user_that_we_already_follows(self):
        """
        status_code returns a 400 BAD REQUEST status response when a user
        try to follows a user that he's already follows.
        """
        requested_data = {"action": "FOLLOW", "follow_uuid": self.follower_uuid}
        patch_url = reverse("api:user-detail", kwargs={"uuid": self.uuid})
        self.client.patch(patch_url, requested_data)
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_nonexistent_user(self):
        """
        status_code returns a 400 BAD REQUEST status response when a user try
        to follow a non-existent user.
        """
        requested_data = {"action": "UNFOLLOW", "follow_uuid": self.follower_uuid}
        patch_url = reverse("api:user-detail", kwargs={"uuid": self.uuid})
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_existent_user(self):
        """
        status_code returns a 200 OK status response when a user unfollows
        another user.
        """
        requested_data = {"action": "FOLLOW", "follow_uuid": self.follower_uuid}
        patch_url = reverse("api:user-detail", kwargs={"uuid": self.uuid})
        self.client.patch(patch_url, requested_data)
        requested_data = {"action": "UNFOLLOW", "follow_uuid": self.follower_uuid}
        patch_url = reverse("api:user-detail", kwargs={"uuid": self.uuid})
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        unfollowed_user = get_user_model().objects.get(uuid=self.follower_uuid)
        self.assertEqual(unfollowed_user.followers.count(), 0)
