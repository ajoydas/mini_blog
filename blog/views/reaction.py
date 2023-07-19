from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post, Reaction


class ReactionView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return []

    def get(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        return Response(post.get_reaction_count())

    def post(self, request, post_id, reaction_type):
        if reaction_type not in ['like', 'dislike']:
            return Response({'error': 'Reaction type must be either like or dislike.'},
                            status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, post_id=post_id)
        user = request.user
        reaction = Reaction.objects.create(post=post, user=user, reaction_type=reaction_type)
        return Response(post.get_reaction_count())

    def delete(self, request, post_id, reaction_type):
        if reaction_type not in ['like', 'dislike']:
            return Response({'error': 'Reaction type must be either like or dislike.'},
                            status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, post_id=post_id)
        user = request.user
        reaction = Reaction.objects.filter(post=post, user=user, reaction_type=reaction_type)
        if reaction is None:
            return Response({'error': 'No reactions exist of the requested type.'}, status=status.HTTP_400_BAD_REQUEST)
        reaction.delete()
        return Response(post.get_reaction_count())
