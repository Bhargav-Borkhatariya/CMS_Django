from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserViewSetTests(TestCase):
    counter = 0 

    def setUp(self):
        UserViewSetTests.counter += 1
        self.client = APIClient()
        self.user_data = {
            'username': f'testuser{UserViewSetTests.counter}',
            'email': f'test{UserViewSetTests.counter}@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_create_user(self):
        url = reverse('user-list')
        new_user_data = {
            'username': 'uniqueuser',
            'email': 'unique@example.com',
            'password': 'securepassword',
            'first_name': 'Unique',
            'last_name': 'User',
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'Account created successfully')
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_validation_error(self):
        url = reverse('user-list')
        invalid_data = {
            'username': self.user.username,  # Duplicate username
            'email': 'not_an_email',  # Invalid email format
            'password': 'short',
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_login(self):
        url = reverse('user-login')
        response = self.client.post(url, {'login': self.user.username, 'password': self.user_data['password']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Login successful')
        self.assertIn('access', response.data["data"])
        self.assertIn('refresh', response.data["data"])

    def test_login_invalid_credentials(self):
        url = reverse('user-login')
        response = self.client.post(url, {'login': self.user.username, 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_me(self):
        url = reverse('user-me')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'User information retrieved')
        self.assertEqual(response.data['data']['username'], self.user.username)

    def test_me_unauthenticated(self):
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        updated_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Account updated successfully')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_update_user_unauthenticated(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        delete_user_data = {
            'username': 'deleteuser',
            'email': 'delete@example.com',
            'password': 'testpassword',
            'first_name': 'Delete',
            'last_name': 'User',
        }
        delete_user = User.objects.create_user(**delete_user_data)
        delete_refresh = RefreshToken.for_user(delete_user)
        delete_access_token = str(delete_refresh.access_token)

        url = reverse('user-detail', kwargs={'pk': delete_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {delete_access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user_unauthenticated(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
