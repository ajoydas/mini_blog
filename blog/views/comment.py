from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from blog.models import Comment, Post
from blog.permissions import IsPostOwnerOrAdmin
from blog.serializers import CommentSerializer, InputParamSerializer
from blog.utils import CommentCreationRateThrottle
from mini_blog.errors import BadRequest


class CommentView(APIView):
    """
    This class handles the GET, POST and DELETE requests for the Comment model.
    """

    def get_throttles(self):
        if self.request.method == 'POST':
            return [CommentCreationRateThrottle()]
        else:
            return [AnonRateThrottle(), UserRateThrottle()]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsPostOwnerOrAdmin()]
        return []

    def get(self, request, comment_id):
        """
        Comment retrieval API.

        This method retrieves a specific comment.
        Paramers:
            request (Request): Request object
            comment_id (int): Comment id
        Returns:
            Response: Specific comment
        """
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request):
        """
        Comment creation API.

        This method creates a new comment.
        Parameters:
            request (Request): Request object containing comment data.
        Returns:
            Response: Newly created comment
        """
        data = request.data.copy()
        comment_id = data.pop('comment_id', None)
        post_id = data.pop('post_id', None)
        input_request = InputParamSerializer(data={'comment_id': comment_id,
                                                   'post_id': post_id})
        input_request.is_valid(raise_exception=True)

        if comment_id:
            parent_comment = get_object_or_404(Comment, pk=input_request.data['comment_id'])
            data['parent'] = parent_comment.comment_id
            data['post'] = parent_comment.post_id
        else:
            post = get_object_or_404(Post, pk=input_request.data['post_id'])
            data['post'] = post.post_id

        data['owner'] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

        raise BadRequest(serializer.errors)

    def delete(self, request, comment_id):
        """
        Comment deletion API.

        This method deletes a specific comment.
        Parameters:
            request (Request): Request object
            comment_id (int): Comment id
        Returns:
            Response: 204 after successful deletion
        """
        comment = get_object_or_404(Comment, comment_id=comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    """
    This class handles the Comment List Retrieval API.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, comment_id=None, post_id=None):
        """
        Comment/Reply list retrieval API.

        Get comments/replies based on comment ID or post ID.
        Parameters:
            request (Request): Request object
            comment_id (int): Comment id
            post_id (int): Post id
        Returns:
            Response: List of post comments or comment replies
        """
        InputParamSerializer(data={'comment_id': comment_id, 'post_id': post_id}) \
            .is_valid(raise_exception=True)

        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            serializer = CommentSerializer(comment.get_replies(), many=True)
            return Response(serializer.data)
        else:
            post = get_object_or_404(Post, pk=post_id)
            serializer = CommentSerializer(post.get_comments(), many=True)
            return Response(serializer.data)
