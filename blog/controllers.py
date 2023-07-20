from django.db import IntegrityError

from blog.models import Reaction


class ReactionAlreadyExistsException(Exception):
    def __init__(self, message="Reaction already exists"):
        self.message = message
        super().__init__(message)


class ReactionController:
    """
    Controller to handle interactions with Reaction model.
    """

    @staticmethod
    def create_reaction(post=None, comment=None, user=None, reaction_type=None):
        try:
            if post:
                return Reaction.objects.create(post=post, user=user, reaction_type=reaction_type)
            else:
                return Reaction.objects.create(comment=comment, user=user, reaction_type=reaction_type)
        except IntegrityError:
            raise ReactionAlreadyExistsException

    @staticmethod
    def delete_reaction(reaction):
        reaction.delete()

    @staticmethod
    def get_reaction_count(post=None, comment=None):
        if post:
            return post.get_reaction_count()
        elif comment:
            return comment.get_reaction_count()
