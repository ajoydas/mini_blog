from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

from blog.controllers import ReactionController, ReactionAlreadyExistsException
from blog.models import Post, Reaction, Comment
from blog.permissions import IsReactionOwner
from blog.serializers import InputParamSerializer, ReactionInputParamSerializer
from mini_blog.errors import BadRequest

ReactionNotExistException = BadRequest('No reactions exist of the requested type.')


class ReactionView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsReactionOwner()]
        return []

    def get(self, request, post_id=None, comment_id=None):
        """
        Reaction count retrieval API.

        This method retrieves the reaction count of a specific post or comment.
        Paramerters:
            request (Request): Request object
            post_id (int): Post id
            comment_id (int): Comment id
        Returns:
            Response: Reaction count of the post or comment.
        """
        InputParamSerializer(data={'comment_id': comment_id, 'post_id': post_id}).is_valid(raise_exception=True)

        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            return Response(ReactionController.get_reaction_count(post=post))
        else:
            comment = get_object_or_404(Comment, pk=comment_id)
            return Response(ReactionController.get_reaction_count(comment=comment))

    def post(self, request, post_id=None, comment_id=None, reaction_type=None):
        """
        Reaction addition API.

        This method adds a reaction to a specific post or comment.
        Parameters:
            request (Request): Request object
            post_id (int): Post id
            comment_id (int): Comment id
            reaction_type (str): Reaction type
        Returns:
            Response: Reaction count of the post or comment.
        """
        ReactionInputParamSerializer(
            data={'comment_id': comment_id, 'post_id': post_id, 'reaction_type': reaction_type}).is_valid(
            raise_exception=True)

        user = request.user
        try:
            if post_id:
                post = get_object_or_404(Post, pk=post_id)
                _ = ReactionController.create_reaction(post=post, user=user, reaction_type=reaction_type)
                return Response(ReactionController.get_reaction_count(post=post))
            else:
                comment = get_object_or_404(Comment, pk=comment_id)
                _ = ReactionController.create_reaction(comment=comment, user=user, reaction_type=reaction_type)
                return Response(ReactionController.get_reaction_count(comment=comment))
        except ReactionAlreadyExistsException as e:
            raise BadRequest(e.message)

    def delete(self, request, post_id=None, comment_id=None, reaction_type=None):
        """
        Reaction deletion API.

        This method deletes a reaction from a specific post or comment.
        Parameters:
            request (Request): Request object
            post_id (int): Post id
            comment_id (int): Comment id
            reaction_type (str): Reaction type
        Returns:
            Response: 204 after successful deletion.
        """
        ReactionInputParamSerializer(
            data={'comment_id': comment_id, 'post_id': post_id, 'reaction_type': reaction_type}).is_valid(
            raise_exception=True)

        user = request.user
        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            try:
                reaction = Reaction.objects.filter(post=post, user=user, reaction_type=reaction_type).get()
                self.check_object_permissions(request, reaction)
                ReactionController.delete_reaction(reaction)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Reaction.DoesNotExist or Reaction.MultipleObjectsReturned:
                raise ReactionNotExistException

        else:
            comment = get_object_or_404(Comment, pk=comment_id)
            try:
                reaction = Reaction.objects.filter(comment=comment, user=user, reaction_type=reaction_type).get()
                self.check_object_permissions(request, reaction)
                ReactionController.delete_reaction(reaction)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Reaction.DoesNotExist or Reaction.MultipleObjectsReturned:
                raise ReactionNotExistException
