from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from blog.models import Post
from blog.permissions import IsAuthor, IsPostOwnerOrAdmin
from blog.serializers import PostSerializer
from blog.utils import PostCreationRateThrottle
from mini_blog.errors import BadRequest


class PostView(APIView):
    """
    This class handles the creation, retrieval, update and deletion of posts.
    """

    def get_throttles(self):
        if self.request.method == 'POST':
            return [PostCreationRateThrottle()]
        else:
            return [AnonRateThrottle(), UserRateThrottle()]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAuthor()]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsPostOwnerOrAdmin()]
        return []

    def get(self, request, post_id=None):
        """
        Post retrieval API.

        This method specific post or post list.
        Parameters:
            request (Request): Request object
            post_id (int): Post id
        Returns:
            Response: Specific Post or the list of all posts
        """
        if post_id is not None:
            post = get_object_or_404(Post, post_id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

    def post(self, request):
        """
        Post creation API.

        This method creates a new post.
        Parameters:
            request (Request): Request object containing post data.
        Returns:
            Response: Newly created post
        """
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        raise BadRequest(serializer.errors)

    def put(self, request, post_id):
        """
        Post update API.

        This method updates an existing post.
        Parameters:
            request (Request): Request object containing post data.
            post_id (int): Post id
        Returns:
            Response: Updated post
        """
        post = get_object_or_404(Post, post_id=post_id)
        data = request.data.copy()
        data['owner'] = post.owner.id
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            self.check_object_permissions(request, post)
            serializer.save()
            return Response(serializer.data)
        raise BadRequest(serializer.errors)

    def delete(self, request, post_id):
        """
        Post deletion API.

        This method deletes an existing post.
        Parameters:
            request (Request): Request object
            post_id (int): Post id
        Returns:
            Response: 204 after successful deletion
        """
        post = get_object_or_404(Post, post_id=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
