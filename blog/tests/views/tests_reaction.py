from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Post, Comment, Reaction


class ReactionViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.post = Post.objects.create(owner=self.user, title='Test Post', body='Test Body')
        self.comment = Comment.objects.create(owner=self.user, post=self.post, body='Test Comment')

    def test_get_reaction_count_for_post(self):
        url = reverse('post-reaction', args=[self.post.post_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {'like': 0, 'dislike': 0}
        self.assertEqual(response.data, expected_data)

    def test_get_reaction_count_for_comment(self):
        url = reverse('comment-reaction', args=[self.comment.comment_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {'like': 0, 'dislike': 0}
        self.assertEqual(response.data, expected_data)

    def test_create_reaction_for_post(self):
        self.client.force_login(self.user)
        url = reverse('post-reaction-interact', args=[self.post.post_id, 'like'])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {'like': 1, 'dislike': 0}
        self.assertEqual(response.data, expected_data)

    def test_create_reaction_for_comment(self):
        self.client.force_login(self.user)
        url = reverse('comment-reaction-interact', args=[self.comment.comment_id, 'dislike'])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {'like': 0, 'dislike': 1}
        self.assertEqual(response.data, expected_data)

    def test_delete_reaction_for_post(self):
        reaction = Reaction.objects.create(post=self.post, user=self.user, reaction_type='like')
        url = reverse('post-reaction-interact', args=[self.post.post_id, reaction.reaction_type])
        self.client.force_login(self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {'like': 0, 'dislike': 0}
        self.assertEqual(response.data, expected_data)

    def test_delete_reaction_for_comment(self):
        reaction = Reaction.objects.create(comment=self.comment, user=self.user, reaction_type='dislike')
        url = reverse('comment-reaction-interact', args=[self.comment.comment_id, reaction.reaction_type])
        self.client.force_login(self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {'like': 0, 'dislike': 0}
        self.assertEqual(response.data, expected_data)

    def test_delete_nonexistent_reaction(self):
        url = reverse('comment-reaction-interact', args=[self.post.post_id, 'dislike'])
        self.client.force_login(self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'No reactions exist of the requested type.'})
