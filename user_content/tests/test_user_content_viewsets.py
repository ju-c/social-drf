from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient
from user_content.models import Post, Comment
from utils.tests.login import Login


class PostViewSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass123", username="HelloThere"
        )
        Post.objects.create(content="This is a post content!", user=test_user)
        Comment.objects.create(
            content="This is a comment content!",
            user=test_user,
            post=Post.objects.get(pk=1),
        )

    def setUp(self) -> None:
        access_token = Login.get_user_access_token("test@test.com", "testpass123").get(
            "access"
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_post_partial_update(self):
        patch_url = reverse("api:post-detail", args=[1])
        requested_data = {"content": "This is an updated post content!"}
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_post = Post.objects.get(pk=1)
        self.assertEqual(updated_post.content, "This is an updated post content!")

    def test_like_on_post_partial_update(self):
        patch_url = reverse("api:post-detail", args=[1])
        requested_data = {"action": "LIKE"}
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_on_post_partial_update(self):
        patch_url = reverse("api:post-detail", args=[1])
        requested_data = {"action": "UNLIKE"}
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_action_serializer(self):
        patch_url = reverse("api:post-detail", args=[1])
        requested_data = {"action": "NOT_LIKE_OR_UNLIKE"}
        response = self.client.patch(patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_partial_update(self):
        comment_patch_url = reverse("api:comment-detail", args=[1])
        requested_data = {"content": "This is an updated comment content!"}
        response = self.client.patch(comment_patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_post = Comment.objects.get(pk=1)
        self.assertEqual(updated_post.content, "This is an updated comment content!")

    def test_like_on_comment_partial_update(self):
        comment_patch_url = reverse("api:comment-detail", args=[1])
        requested_data = {"action": "LIKE"}
        response = self.client.patch(comment_patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_on_comment_partial_update(self):
        comment_patch_url = reverse("api:comment-detail", args=[1])
        requested_data = {"action": "UNLIKE"}
        response = self.client.patch(comment_patch_url, requested_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
