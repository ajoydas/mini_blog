from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Comment, Post
from blog.serializers import CommentSerializer


class CommentViewTestCase(APITestCase):
    """
    This testcase tests the comment APIs.
    """

    def setUp(self):
        self.reader = User.objects.create_user(username='testuser', password='testpass')
        self.reader.profile.role = 'Reader'
        self.reader.save()
        self.admin = User.objects.create_user(username='admin', password='adminpass')
        self.admin.profile.role = 'Admin'
        self.admin.save()

        self.post = Post.objects.create(owner=self.admin, title='Test Post', body='Test Body')

        self.comment = Comment.objects.create(owner=self.reader, post=self.post, body='Test Comment')

    def test_retrieve_comment(self):
        url = reverse('comment-detail', args=[self.comment.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['owner'], self.comment.owner.id)
        self.assertEqual(response.data['body'], self.comment.body)

    def test_add_post_comment(self):
        url = reverse('comment-route')
        data = {'body': 'New Comment', 'post_id': self.post.pk}
        self.client.force_authenticate(user=self.reader)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_comment = Comment.objects.get(pk=response.data['comment_id'])
        self.assertEqual(created_comment.owner, self.reader)
        self.assertEqual(created_comment.body, data['body'])

    def test_add_comment_reply(self):
        url = reverse('comment-route')
        data = {'body': 'New Comment', 'comment_id': self.comment.pk}
        self.client.force_authenticate(user=self.reader)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_comment = Comment.objects.get(pk=response.data['comment_id'])
        self.assertEqual(created_comment.owner, self.reader)
        self.assertEqual(created_comment.body, data['body'])

    def test_add_post_comment_unauthenticated_user(self):
        url = reverse('comment-route')
        data = {'body': 'New Comment', 'post_id': self.post.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_as_admin(self):
        url = reverse('comment-detail', args=[self.comment.pk])
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that the comment is deleted
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_as_comment_author(self):
        url = reverse('comment-detail', args=[self.comment.pk])
        self.client.force_authenticate(user=self.reader)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that the comment is deleted
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())


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
