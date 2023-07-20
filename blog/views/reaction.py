from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post, Reaction, Comment


class IsReactionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ReactionView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsReactionOwner()]
        return []

    def get(self, request, post_id=None, comment_id=None):
        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            return Response(post.get_reaction_count())
        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            return Response(comment.get_reaction_count())
        return Response({'error': 'Either post_id or comment_id should be set.'},
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, post_id=None, comment_id=None, reaction_type=None):
        if not reaction_type and reaction_type not in ['like', 'dislike']:
            return Response({'error': 'Reaction type must be either like or dislike.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if post_id:
            post = get_object_or_404(Post, post_id=post_id)
            _ = Reaction.objects.create(post=post, user=user, reaction_type=reaction_type)
            return Response(post.get_reaction_count())
        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            _ = Reaction.objects.create(comment=comment, user=user, reaction_type=reaction_type)
            return Response(comment.get_reaction_count())
        return Response({'error': 'Either post_id or comment_id should be set.'},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id=None, comment_id=None, reaction_type=None):
        if reaction_type not in ['like', 'dislike']:
            return Response({'error': 'Reaction type must be either like or dislike.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if post_id:
            post = get_object_or_404(Post, post_id=post_id)
            try:
                reaction = Reaction.objects.filter(post=post, user=user, reaction_type=reaction_type).get()
                self.check_object_permissions(request, reaction)
                reaction.delete()
                return Response(post.get_reaction_count())
            except Reaction.DoesNotExist or Reaction.MultipleObjectsReturned:
                return Response({'error': 'No reactions exist of the requested type.'},
                                status=status.HTTP_400_BAD_REQUEST)
        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            try:
                reaction = Reaction.objects.filter(comment=comment, user=user, reaction_type=reaction_type).get()
                self.check_object_permissions(request, reaction)
                reaction.delete()
                return Response(comment.get_reaction_count())
            except Reaction.DoesNotExist or Reaction.MultipleObjectsReturned:
                return Response({'error': 'No reactions exist of the requested type.'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Either post_id or comment_id should be set.'},
                        status=status.HTTP_400_BAD_REQUEST)
