from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class BlogAPITestCase(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='password', role='author')
        self.reader = User.objects.create_user(username='reader', password='password', role='reader')
        self.admin = User.objects.create_superuser(username='admin', password='password', role='admin')

    def test_register_user(self):
        url = '/api/register/'
        data = {'username': 'newuser', 'password': 'password', 'role': 'reader'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = '/api/login/'
        data = {'username': 'reader', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
