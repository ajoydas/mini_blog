from django.shortcuts import get_object_or_404
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

    def get(self, request, comment_id=None, post_id=None):
        if comment_id:
            comment = get_object_or_404(Comment, post_id=comment_id)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            serializer = CommentSerializer(post.get_comments(), many=True)
            return Response(serializer.data)

        return Response({'error': 'Either parent_id or post_id must be provided.'},
                        status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, comment_id=None, post_id=None):
        data = request.data.copy()

        if comment_id:
            parent_comment = get_object_or_404(Comment, pk=comment_id)
            data['parent'] = parent_comment
        elif post_id:
            post = get_object_or_404(Post, pk=post_id)
            data['post'] = post
        else:
            return Response({'error': 'Either parent_id or post_id must be provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data['owner'] = request.user.id

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, comment_id=comment_id)
        # self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, post_id=comment_id)
        serializer = CommentSerializer(comment.get_replies(), many=True)
        return Response(serializer.data)
