from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Post, Comment, Reaction


class PostModelTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(owner=self.user, title='Test Post', body='Test Body')

    def test_get_comments(self):
        # Create comments associated with the post
        comment1 = Comment.objects.create(owner=self.user, post=self.post, body='Comment 1')
        comment2 = Comment.objects.create(owner=self.user, post=self.post, body='Comment 2')

        # Call get_comments() on the post instance
        comments = self.post.get_comments()

        # Assert that both comments are retrieved
        self.assertEqual(comments.count(), 2)
        self.assertIn(comment1, comments)
        self.assertIn(comment2, comments)

    def test_get_reaction_count(self):
        # Create reactions associated with the post
        _ = Reaction.objects.create(post=self.post, user=self.user, reaction_type='like')
        _ = Reaction.objects.create(post=self.post, user=self.user, reaction_type='dislike')

        # Call get_reaction_count() on the post instance
        reaction_count = self.post.get_reaction_count()

        # Assert that the reaction count is as expected
        self.assertEqual(reaction_count['like'], 1)
        self.assertEqual(reaction_count['dislike'], 1)
