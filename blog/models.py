from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


class Post(models.Model):
    """
    Model to represent a blog post.
    """
    post_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Owner: {self.owner.username}, Post: {self.title}'

    def get_comments(self):
        """
        Returns comments on the post.
        """
        return list(Comment.objects.filter(post=self, parent=None))

    def get_reaction_count(self):
        """
        Returns the number of likes and dislikes on the post.
        """
        reactions = (
            Reaction.objects
            .filter(post=self)
            .values('reaction_type')
            .annotate(count=Count('reaction_type'))
        )

        reaction_count = {
            'like': 0,
            'dislike': 0,
        }
        for reaction in reactions:
            reaction_count[reaction['reaction_type']] = reaction['count']

        return reaction_count


class Comment(models.Model):
    """
    Model to represent a comment on a blog post.
    """
    comment_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def get_replies(self):
        """
           Returns a queryset of immediate child comments.
       """
        return list(Comment.objects.filter(parent=self))

    def get_reaction_count(self):
        """
        Returns the number of likes and dislikes on the comment.
        """
        reactions = (
            Reaction.objects
            .filter(comment=self)
            .values('reaction_type')
            .annotate(count=Count('reaction_type'))
        )
        reaction_count = {
            'like': 0,
            'dislike': 0,
        }
        for reaction in reactions:
            reaction_count[reaction['reaction_type']] = reaction['count']

        return reaction_count


class Reaction(models.Model):
    """
    Model to represent a reaction to a blog post or comment.
    """
    # two types of reactions: like and dislike
    REACTION_CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['post', 'user', 'reaction_type'], ['comment', 'user', 'reaction_type']]
