from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Comment, Post
from blog.serializers import CommentSerializer


# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#     def get_permissions(self):
#         if self.action in ['view']:
#             return [permissions.AllowAny]
#         if self.action in ['create']:
#             return [permissions.IsAuthenticated()]
#         return []

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'Admin'


class CommentView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsAdmin()]
        return []

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, post_id=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        parent_id = data.pop('parent_id', None)
        post_id = data.pop('post_id', None)

        if parent_id:
            parent_comment = get_object_or_404(Comment, pk=parent_id[0])
            data['parent'] = parent_comment.comment_id
            data['post'] = parent_comment.post_id
        elif post_id:
            post = get_object_or_404(Post, pk=post_id[0])
            data['post'] = post.post_id
        else:
            return Response({'error': 'Either parent_id or post_id must be provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data['owner'] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, comment_id=comment_id)
        # self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'comment_id',
                openapi.IN_QUERY,
                description='Comment ID. Retrieve comments for a specific comment ID.',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'post_id',
                openapi.IN_QUERY,
                description='Post ID. Retrieve comments for a specific post ID.',
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            status.HTTP_200_OK: CommentSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_404_NOT_FOUND: 'Not Found'
        }
    )
    def get(self, request, comment_id=None, post_id=None):
        """
        Get comments based on comment ID or post ID.

        Parameters:
        - comment_id: Comment ID (optional)
        - post_id: Post ID (optional)
        """
        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            serializer = CommentSerializer(comment.get_replies(), many=True)
            return Response(serializer.data)
        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            serializer = CommentSerializer(post.get_comments(), many=True)
            return Response(serializer.data)

        return Response({'error': 'Either parent_id or post_id must be provided.'},
                        status=status.HTTP_400_BAD_REQUEST)
