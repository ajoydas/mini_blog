from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import PostSerializer


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get_permissions(self):
#         if self.action in ['view']:
#             return [permissions.AllowAny]
#         if self.action in ['create']:
#             return [permissions.IsAuthenticated()]
#         elif self.action in ['update', 'partial_update', 'destroy']:
#             post = self.get_object()
#             if self.request.user == post.owner or self.request.user.profile.role == 'Admin':
#                 return [permissions.IsAuthenticated()]
#         return []

class IsPostOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print('checking is object permission', obj.owner == request.user, request.user.profile.role == 'Admin')
        return obj.owner == request.user or request.user.profile.role == 'Admin'


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        # print('checking is author: ', request.user.profile.role)
        return request.user.profile.role == 'Author'


# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.profile.role == 'Admin'


class PostView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAuthor()]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsPostOwnerOrAdmin()]
        return []

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({'error': 'Permission denied. You are not authorized to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)
        elif isinstance(exc, NotAuthenticated):
            return Response({'error': 'Permission denied. You should be authenticated to perform this action.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)

    def get(self, request, post_id=None):
        if post_id is not None:
            post = get_object_or_404(Post, post_id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

    def post(self, request):
        # title = request.data.get('title')
        # body = request.data.get('body')
        # self.check_permissions(request)
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            self.check_object_permissions(request, post)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
