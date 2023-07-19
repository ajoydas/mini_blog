from django.test import TestCase

from .models import Reaction, Post, Comment, User


class ReactionModelTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Test Post')
        self.comment = Comment.objects.create(content='Test Comment')

    def test_unique_reaction_with_post(self):
        # Create a reaction with a post and user
        reaction = Reaction.objects.create(post=self.post, user=self.user)

        # Try to create another reaction with the same post and user
        with self.assertRaises(Exception):
            Reaction.objects.create(post=self.post, user=self.user)

    def test_unique_reaction_with_comment(self):
        # Create a reaction with a comment and user
        reaction = Reaction.objects.create(comment=self.comment, user=self.user)

        # Try to create another reaction with the same comment and user
        with self.assertRaises(Exception):
            Reaction.objects.create(comment=self.comment, user=self.user)

    def test_unique_reaction_with_both_post_and_comment(self):
        # Try to create a reaction with both post and comment (should raise an exception)
        with self.assertRaises(Exception):
            Reaction.objects.create(post=self.post, comment=self.comment, user=self.user)
