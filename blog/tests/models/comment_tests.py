from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Post, Comment


class CommentModelTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Test Post', owner=self.user)
        self.parent_comment = Comment.objects.create(owner=self.user, post=self.post, body='Parent Comment')
        self.child_comment1 = Comment.objects.create(owner=self.user, post=self.post, body='Child Comment 1',
                                                     parent=self.parent_comment)
        self.child_comment2 = Comment.objects.create(owner=self.user, post=self.post, body='Child Comment 2',
                                                     parent=self.parent_comment)
        self.orphan_comment = Comment.objects.create(owner=self.user, post=self.post, body='Orphan Comment')

    def test_get_child_comments(self):
        # Get child comments for the parent comment
        child_comments = self.parent_comment.get_replies()

        # Assert that the child comments are correctly retrieved
        self.assertEqual(child_comments.count(), 2)
        self.assertIn(self.child_comment1, child_comments)
        self.assertIn(self.child_comment2, child_comments)

    def test_get_child_comments_with_no_children(self):
        # Get child comments for the orphan comment
        child_comments = self.orphan_comment.get_replies()

        # Assert that no child comments are retrieved
        self.assertEqual(child_comments.count(), 0)
