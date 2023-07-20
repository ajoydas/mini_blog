from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Comment, Post
from blog.serializers import CommentSerializer


class CommentViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.profile.role = 'Reader'
        self.user.save()
        self.admin = User.objects.create_user(username='admin', password='adminpass')
        self.admin.profile.role = 'Admin'
        self.admin.save()
        # Create a test post
        self.post = Post.objects.create(owner=self.admin, title='Test Post', body='Test Body')

        # Create a test comment
        self.comment = Comment.objects.create(owner=self.user, post=self.post, body='Test Comment')

    def test_retrieve_comment(self):
        url = reverse('comment-detail', args=[self.comment.pk])
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the retrieved comment data matches the expected data
        self.assertEqual(response.data['owner'], self.comment.owner.id)
        self.assertEqual(response.data['body'], self.comment.body)

    def test_add_post_comment(self):
        url = reverse('comment-route')
        data = {'body': 'New Comment', 'post_id': self.post.pk}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the created comment matches the expected data
        created_comment = Comment.objects.get(pk=response.data['comment_id'])
        self.assertEqual(created_comment.owner, self.user)
        self.assertEqual(created_comment.body, data['body'])

    def test_add_comment_reply(self):
        url = reverse('comment-route')
        data = {'body': 'New Comment', 'parent_id': self.comment.pk}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the created comment matches the expected data
        created_comment = Comment.objects.get(pk=response.data['comment_id'])
        self.assertEqual(created_comment.owner, self.user)
        self.assertEqual(created_comment.body, data['body'])

    def test_add_post_comment_unauthenticated_user(self):
        url = reverse('comment-route')
        data = {'body': 'New Comment', 'post_id': self.post.pk}
        response = self.client.post(url, data)

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_as_admin(self):
        url = reverse('comment-detail', args=[self.comment.pk])
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)

        # Assert that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that the comment is deleted
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_as_non_admin(self):
        url = reverse('comment-detail', args=[self.comment.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        # Assert that the response status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Assert that the comment is not deleted
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())


class CommentListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(owner=self.user, title='Test Post', body='Test Body')
        self.comment = Comment.objects.create(owner=self.user, post=self.post, body='Test Comment')
        self.child_comment1 = Comment.objects.create(owner=self.user, post=self.post, body='Child Comment 1')
        self.child_comment2 = Comment.objects.create(owner=self.user, parent=self.comment, post=self.post,
                                                     body='Child Comment 2')
        self.child_comment3 = Comment.objects.create(owner=self.user, parent=self.comment, post=self.post,
                                                     body='Child Comment 3')

    def test_get_comments_by_comment_id(self):
        url = reverse('comment-replies', args=[self.comment.comment_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CommentSerializer([self.child_comment2, self.child_comment3], many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_comments_by_post_id(self):
        url = reverse('post-comments', args=[self.post.post_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CommentSerializer([self.comment, self.child_comment1], many=True)
        self.assertEqual(response.data, serializer.data)


def test_get_comments_missing_ids(self):
    url = reverse('comment-replies')
    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {'error': 'Either parent_id or post_id must be provided.'})

# class CommentListViewTestCase(APITestCase):
#     @patch('django.shortcuts.get_object_or_404')
#     def test_get_replies_for_comment(self, mock_get_object_or_404):
#         # Mock get_object_or_404 to return a comment
#         mock_comment = Comment(owner=User(id=1), body='Test Comment')
#         mock_get_object_or_404.return_value = mock_comment
#
#         url = reverse('comment-route', args=[1])
#         response = self.client.get(url)
#
#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)
#
#         # Assert that the retrieved comment data matches the expected data
#         self.assertEqual(response.data['owner'], mock_comment.owner)
#         self.assertEqual(response.data['body'], mock_comment.body)
#
#         # Verify that get_object_or_404 was called with the correct arguments
#         mock_get_object_or_404.assert_called_once_with(Comment, post_id=1)
#
#     from unittest.mock import patch
#
#     @patch('django.shortcuts.get_object_or_404')
#     def test_get_comments_for_post(self, mock_get_object_or_404):
#         # Mock get_object_or_404 to return a post
#         mock_user = User(id=1, username='test_user')
#         mock_post = Post(owner=mock_user, title='Test Post', body='Test Body')
#         mock_get_object_or_404.return_value = mock_post
#
#         # Mock the Comment.objects.filter method to return a list of comments
#         mock_comments = [
#             Comment(owner=mock_user, post=mock_post, body='Test Comment 1'),
#             Comment(owner=mock_user, post=mock_post, body='Test Comment 2')
#         ]
#         mock_post.get_comments.return_value = mock_comments
#
#         url = reverse('post-comments', args=[1])
#         response = self.client.get(url)
#
#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)
#
#         # Assert that the number of retrieved comments matches the expected count
#         self.assertEqual(len(response.data), 2)
#
#         # Verify that get_object_or_404 was called with the correct arguments
#         mock_get_object_or_404.assert_called_once_with(Post, post_id=1)
#
#         # Verify that the get_comments method was called on the mock_post object
#         mock_post.get_comments.assert_called_once()
#
#         # Verify that the filter method was called on the mock_comments queryset
#         mock_post.get_comments.return_value.filter.assert_called_once()
#
#     def test_get_comments_with_missing_parameter(self):
#         url = reverse('get_comments_for_post', args=[1])
#         response = self.client.get(url)
#
#         # Assert that the response status code is 400 (Bad Request)
#         self.assertEqual(response.status_code, 400)
