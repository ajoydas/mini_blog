from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Post


class PostViewTestCase(APITestCase):
    """
    This testcase tests the post APIs.
    """

    def setUp(self):
        self.reader = User.objects.create_user(username='reader', password='testpass')
        self.reader.profile.role = 'Reader'
        self.reader.save()
        self.author = User.objects.create_user(username='author', password='testpass')
        self.author.profile.role = 'Author'
        self.author.save()
        self.admin = User.objects.create_user(username='admin', password='adminpass')
        self.admin.profile.role = 'Admin'
        self.admin.save()

        self.post = Post.objects.create(owner=self.author, title='Test Post', body='Test Body')

    def test_get_single_post_by_unauthenticated_user(self):
        url = reverse('post-detail', args=[self.post.post_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_by_author_user(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'body': 'New Body'}
        self.client.force_authenticate(user=self.author)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_post = Post.objects.get(pk=response.data['post_id'])
        self.assertEqual(created_post.owner, self.author)
        self.assertEqual(created_post.title, data['title'])
        self.assertEqual(created_post.body, data['body'])

    def test_create_post_by_unauthenticated_user(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'body': 'New Body'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_by_non_author_user(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'body': 'New Body'}
        self.client.force_authenticate(user=self.reader)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_by_owner(self):
        url = reverse('post-detail', args=[self.post.post_id])
        data = {'title': 'Updated Post', 'body': 'Updated Body'}
        self.client.force_authenticate(user=self.author)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_post = Post.objects.get(pk=self.post.post_id)
        self.assertEqual(updated_post.title, data['title'])
        self.assertEqual(updated_post.body, data['body'])

    def test_update_post_by_admin(self):
        url = reverse('post-detail', args=[self.post.post_id])
        data = {'title': 'Updated Post', 'body': 'Updated Body'}
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_post = Post.objects.get(pk=self.post.post_id)
        self.assertEqual(updated_post.title, data['title'])
        self.assertEqual(updated_post.body, data['body'])

    def test_update_post_by_unauthorized_user(self):
        url = reverse('post-detail', args=[self.post.post_id])
        data = {'title': 'Updated Post', 'body': 'Updated Body'}
        self.client.force_authenticate(user=self.reader)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_by_owner(self):
        post = Post.objects.create(owner=self.author, title='Test Post', body='Test Body')
        url = reverse('post-detail', args=[post.post_id])
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Post.objects.filter(pk=post.post_id).exists())

    def test_delete_post_by_admin(self):
        post = Post.objects.create(owner=self.author, title='Test Post', body='Test Body')
        url = reverse('post-detail', args=[post.post_id])
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Post.objects.filter(pk=post.post_id).exists())

    def test_delete_post_by_unauthorized_user(self):
        url = reverse('post-detail', args=[self.post.post_id])
        self.client.force_authenticate(user=self.reader)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
