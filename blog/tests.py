from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostAPITestCase(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='password')
        self.reader = User.objects.create_user(username='reader', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password')

        self.post = Post.objects.create(title='Test Post', content='Test content', author=self.author)

    def test_list_posts(self):
        url = '/api/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        url = '/api/posts/'
        self.client.login(username='author', password='password')
        data = {'title': 'New Post', 'content': 'New content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post_by_author(self):
        url = f'/api/posts/{self.post.id}/'
        self.client.login(username='author', password='password')
        data = {'title': 'Updated Post', 'content': 'Updated content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_by_admin(self):
        url = f'/api/posts/{self.post.id}/'
        self.client.login(username='admin', password='password')
        data = {'title': 'Updated Post', 'content': 'Updated content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_by_reader(self):
        url = f'/api/posts/{self.post.id}/'
        self.client.login(username='reader', password='password')
        data = {'title': 'Updated Post', 'content': 'Updated content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_by_author(self):
        url = f'/api/posts/{self.post.id}/'
        self.client.login(username='author', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_by_admin(self):
        url = f'/api/posts/{self.post.id}/'
        self.client.login(username='admin', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_by_reader(self):
        url = f'/api/posts/{self.post.id}/'
        self.client.login(username='reader', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_post(self):
        url = f'/api/posts/{self.post.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        url = '/api/comments/'
        self.client.login(username='reader', password='password')
        data = {'content': 'Test comment', 'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reaction(self):
        url = '/api/reactions/'
        self.client.login(username='reader', password='password')
        data = {'reaction_type': 'like', 'post': self.post.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
