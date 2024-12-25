from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Like
from accounts.models import User


class PostViewSetTests(TestCase):
    counter = 0

    def setUp(self):
        PostViewSetTests.counter += 1
        # Create users
        self.user = User.objects.create_user(
            username=f"testuser{PostViewSetTests.counter}",
            email=f"test{PostViewSetTests.counter}@example.com",
            password="testpassword",
        )
        self.other_user = User.objects.create_user(
            username=f"otheruser{PostViewSetTests.counter}",
            email=f"othertest{PostViewSetTests.counter}@example.com",
            password="otherpassword",
        )

        # Set up tokens
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        self.client = APIClient()

        # Create posts
        self.public_post = Post.objects.create(
            title="Public Post",
            description="Public description",
            content="Public content",
            is_public=True,
            author=self.user,
        )
        self.private_post = Post.objects.create(
            title="Private Post",
            description="Private description",
            content="Private content",
            is_public=False,
            author=self.user,
        )

    def test_list_posts(self):
        """Test retrieving the list of public posts"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["data"]), 1
        )  # Only public post should appear
        self.assertEqual(response.data["data"][0]["title"], self.public_post.title)

    def test_retrieve_public_post(self):
        """Test retrieving a public post"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("post-detail", kwargs={"pk": self.public_post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"], self.public_post.title)

    def test_retrieve_private_post_as_owner(self):
        """Test retrieving a private post as the owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("post-detail", kwargs={"pk": self.private_post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"], self.private_post.title)

    def test_retrieve_private_post_as_other_user(self):
        """Test retrieving a private post as a non-owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        other_client = APIClient()
        other_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(RefreshToken.for_user(self.other_user).access_token)}"
        )
        url = reverse("post-detail", kwargs={"pk": self.private_post.pk})
        response = other_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post(self):
        """Test creating a post"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("post-list")
        data = {
            "title": "New Post",
            "description": "New description",
            "content": "New content",
            "is_public": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["title"], data["title"])
        self.assertEqual(Post.objects.count(), 3)

    def test_update_post(self):
        """Test updating a post"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("post-detail", kwargs={"pk": self.public_post.pk})
        data = {
            "title": "Updated Title",
            "description": "Updated description",
            "content": "Updated content",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.public_post.refresh_from_db()
        self.assertEqual(self.public_post.title, "Updated Title")

    def test_delete_post(self):
        """Test deleting a post"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("post-detail", kwargs={"pk": self.public_post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)


class LikeViewSetTests(TestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username=f"testuser{PostViewSetTests.counter}",
            email=f"test{PostViewSetTests.counter}@example.com",
            password="testpassword",
        )
        self.other_user = User.objects.create_user(
            username=f"otheruser{PostViewSetTests.counter}",
            email=f"otheruser{PostViewSetTests.counter}@example.com",
            password="otherpassword",
        )

        # Set up tokens
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        self.client = APIClient()

        # Create post
        self.post = Post.objects.create(
            title="Post to Like",
            description="Description",
            content="Content",
            is_public=True,
            author=self.user,
        )

    def test_like_post(self):
        """Test liking a post"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("like-create", kwargs={"pk": self.post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_post(self):
        """Test unliking a post"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        Like.objects.create(post=self.post, user=self.user)
        url = reverse("like-destroy", kwargs={"pk": self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_like_already_liked_post(self):
        """Test liking an already liked post"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        Like.objects.create(post=self.post, user=self.user)
        url = reverse("like-create", kwargs={"pk": self.post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unlike_not_liked_post(self):
        """Test unliking a post that is not liked"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("like-destroy", kwargs={"pk": self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
