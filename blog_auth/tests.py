from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationViewTest(APITestCase):
    def test_user_registration(self):
        # User should be able to register
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Request failed')
        self.assertEqual(User.objects.count(), 1, 'User is not created')
        self.assertEqual(User.objects.get().username, 'testuser', 'Username does not match')


class UserLoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_login(self):
        # User should be able to login
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Validate access token
        access_token = response.data['access']
        decoded_token = TokenBackend(algorithm='HS256').decode(access_token, verify=False)
        self.assertEqual(decoded_token['user_id'], self.user.id, 'User id in token payload does not match')


class ProfileViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('profile', args=[self.user.username])

        self.profile = self.user.profile
        self.profile.bio = 'Test bio'
        self.profile.role = 'Author'
        self.profile.save()

        # Generate JWT tokens for authentication
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_get_profile(self):
        # User should be able to get their profile
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        expected_data = {
            'id': self.profile.id,
            'bio': self.profile.bio,
            'role': self.profile.role,
            'user': self.profile.user.id,
        }
        self.assertEqual(response.data, expected_data, 'Response does not match with expected profile data')

    def test_update_profile_as_superuser(self):
        # Superuser should be able to update the profile's role
        self.user.is_superuser = True
        self.user.save()

        updated_data = {
            'user': self.user.id,
            'bio': 'Updated bio',
            'role': 'Admin'
        }
        self.client.force_login(self.user)
        response = self.client.put(self.url, data=updated_data)

        self.assertEqual(response.status_code, 200)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.role, 'Admin')

    def test_update_profile_as_non_superuser(self):
        # Non-superuser should not be able to update the profile's role
        self.user.is_superuser = False
        self.user.save()

        updated_data = {
            'user': self.user.id,
            'bio': 'Failed bio',
            'role': 'Failed Role'
        }
        self.client.force_login(self.user)
        response = self.client.put(self.url, data=updated_data)

        self.assertEqual(response.status_code, 400, 'Should not be able to update the profile as a non-superuser')

        self.profile.refresh_from_db()
        self.assertNotEqual(self.profile.bio, 'Failed bio')
        self.assertNotEqual(self.profile.role, 'Failed Role')
