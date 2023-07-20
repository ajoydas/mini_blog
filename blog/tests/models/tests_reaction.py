from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Post, Comment, Reaction


class ReactionModelTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Test Post', owner=self.user)
        self.comment = Comment.objects.create(body='Test Comment', owner=self.user, post=self.post)

    def test_reaction_creation(self):
        # Create a reaction
        reaction = Reaction.objects.create(post=self.post, user=self.user, reaction_type='like')

        # Check if the reaction is created successfully
        self.assertEqual(reaction.post, self.post)
        self.assertEqual(reaction.user, self.user)
        self.assertEqual(reaction.reaction_type, 'like')

    def test_unique_reaction_with_post(self):
        # Create a reaction with a post, user, and reaction_type
        _ = Reaction.objects.create(post=self.post, user=self.user, reaction_type='like')

        # Try to create another reaction with the same post, user, and reaction_type
        with self.assertRaises(Exception):
            Reaction.objects.create(post=self.post, user=self.user, reaction_type='like')

    def test_unique_reaction_with_comment(self):
        # Create a reaction with a comment, user, and reaction_type
        _ = Reaction.objects.create(comment=self.comment, user=self.user, reaction_type='dislike')

        # Try to create another reaction with the same comment, user, and reaction_type
        with self.assertRaises(Exception):
            Reaction.objects.create(comment=self.comment, user=self.user, reaction_type='dislike')

    # def test_reaction_unique_together_post_user_comment_user(self):
    #     # Try to create a reaction with both post and comment and the same user (should raise an exception)
    #     with self.assertRaises(Exception):
    #         Reaction.objects.create(post=self.post, comment=self.comment, user=self.user, reaction_type='like')
