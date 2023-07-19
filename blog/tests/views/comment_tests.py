from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Comment, Post


class CommentViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_user(username='adminuser', password='adminpass')

        # Create a test post
        self.post = Post.objects.create(owner=self.user, title='Test Post', body='Test Body')

        # Create a test comment
        self.comment = Comment.objects.create(owner=self.user, post=self.post, body='Test Comment')

    def test_get_comment(self):
        url = reverse('get_comment', args=[self.comment.pk])
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the retrieved comment data matches the expected data
        self.assertEqual(response.data['owner'], self.comment.owner.username)
        self.assertEqual(response.data['body'], self.comment.body)

    def test_post_comment(self):
        url = reverse('comment_list')
        data = {'body': 'New Comment', 'post_id': self.post.pk}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the created comment matches the expected data
        created_comment = Comment.objects.get(pk=response.data['comment_id'])
        self.assertEqual(created_comment.owner, self.user)
        self.assertEqual(created_comment.body, data['body'])

    def test_delete_comment_as_admin(self):
        url = reverse('delete_comment', args=[self.comment.pk])
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)

        # Assert that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that the comment is deleted
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_as_non_admin(self):
        url = reverse('delete_comment', args=[self.comment.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # Assert that the response status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Assert that the comment is not deleted
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())


class CommentListViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a test post
        self.post = Post.objects.create(owner=self.user, title='Test Post', body='Test Body')

        # Create a test comment
        self.comment = Comment.objects.create(owner=self.user, post=self.post, body='Test Comment')

    def test_get_comment_by_id(self):
        url = reverse('get_comment', args=[self.comment.pk])
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the retrieved comment data matches the expected data
        self.assertEqual(response.data['owner'], self.comment.owner.username)
        self.assertEqual(response.data['body'], self.comment.body)

    def test_get_comments_for_post(self):
        url = reverse('get_comments_for_post', args=[self.post.pk])
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the number of retrieved comments matches the expected count
        self.assertEqual(len(response.data), 1)

    def test_get_comments_for_invalid_post(self):
        url = reverse('get_comments_for_post', args=[999])  # Invalid post ID
        response = self.client.get(url)

        # Assert that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comments_with_missing_parameter(self):
        url = reverse('get_comments_for_post', args=[self.post.pk])
        response = self.client.get(url)

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
