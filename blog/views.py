# from django.shortcuts import get_object_or_404
# from rest_framework import permissions, status
# from rest_framework.response import Response
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
# from rest_framework.views import APIView
#
# from .models import Post, Comment, Reaction
# from .serializers import PostSerializer, ReactionSerializer, CommentSerializer
#
#
# # class PostViewSet(viewsets.ModelViewSet):
# #     queryset = Post.objects.all()
# #     serializer_class = PostSerializer
# #
# #     def get_permissions(self):
# #         if self.action in ['view']:
# #             return [permissions.AllowAny]
# #         if self.action in ['create']:
# #             return [permissions.IsAuthenticated()]
# #         elif self.action in ['update', 'partial_update', 'destroy']:
# #             post = self.get_object()
# #             if self.request.user == post.owner or self.request.user.profile.role == 'Admin':
# #                 return [permissions.IsAuthenticated()]
# #         return []
#
# class IsPostOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user
#
#
# class IsAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.profile.role == 'Admin'
#
#
# class PostView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#     throttle_classes = [AnonRateThrottle, UserRateThrottle]
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         elif self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
#             return [IsPostOwner() or IsAdmin()]
#         return []
#
#     def get(self, request, post_id=None):
#         if post_id is not None:
#             post = get_object_or_404(Post, post_id=post_id)
#             serializer = PostSerializer(post)
#             return Response(serializer.data)
#         else:
#             posts = Post.objects.all()
#             serializer = PostSerializer(posts, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         # title = request.data.get('title')
#         # body = request.data.get('body')
#         data = request.data.copy()
#         data['owner'] = request.user.id
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             post = serializer.save()
#             return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, post_id):
#         post = get_object_or_404(Post, post_id=post_id)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, post_id):
#         post = get_object_or_404(Post, post_id=post_id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# # class CommentViewSet(viewsets.ModelViewSet):
# #     queryset = Comment.objects.all()
# #     serializer_class = CommentSerializer
# #
# #     def get_permissions(self):
# #         if self.action in ['view']:
# #             return [permissions.AllowAny]
# #         if self.action in ['create']:
# #             return [permissions.IsAuthenticated()]
# #         return []
#
# class CommentView(APIView):
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         elif self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         return []
#
#     def get(self, request, comment_id=None):
#         if comment_id is not None:
#             comment = get_object_or_404(Comment, post_id=comment_id)
#             serializer = CommentSerializer(comment)
#             return Response(serializer.data)
#         else:
#             comments = Comment.objects.all()
#             serializer = CommentSerializer(comments, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         data = request.data
#         data['owner'] = request.user.id
#         serializer = CommentSerializer(data=data)
#         if serializer.is_valid():
#             post = serializer.save()
#             return Response(CommentSerializer(post).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ReactionView(APIView):
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         elif self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         return []
#
#     def get(self, request, reaction_id=None):
#         if reaction_id is not None:
#             reaction = get_object_or_404(Reaction, post_id=reaction_id)
#             serializer = ReactionSerializer(reaction)
#             return Response(serializer.data)
#         else:
#             reactions = Reaction.objects.all()
#             serializer = ReactionSerializer(reactions, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         data = request.data
#         data['owner'] = request.user.id
#         serializer = ReactionSerializer(data=data)
#         if serializer.is_valid():
#             post = serializer.save()
#             return Response(ReactionSerializer(post).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# from django.shortcuts import get_object_or_404
# from rest_framework import permissions, status
# from rest_framework.response import Response
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
# from rest_framework.views import APIView
#
# from .models import Post, Comment, Reaction
# from .serializers import PostSerializer, ReactionSerializer, CommentSerializer
#
#
# # class PostViewSet(viewsets.ModelViewSet):
# #     queryset = Post.objects.all()
# #     serializer_class = PostSerializer
# #
# #     def get_permissions(self):
# #         if self.action in ['view']:
# #             return [permissions.AllowAny]
# #         if self.action in ['create']:
# #             return [permissions.IsAuthenticated()]
# #         elif self.action in ['update', 'partial_update', 'destroy']:
# #             post = self.get_object()
# #             if self.request.user == post.owner or self.request.user.profile.role == 'Admin':
# #                 return [permissions.IsAuthenticated()]
# #         return []
#
# class IsPostOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user
#
#
# class IsAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.profile.role == 'Admin'
#
#
# class PostView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#     throttle_classes = [AnonRateThrottle, UserRateThrottle]
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         elif self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
#             return [IsPostOwner() or IsAdmin()]
#         return []
#
#     def get(self, request, post_id=None):
#         if post_id is not None:
#             post = get_object_or_404(Post, post_id=post_id)
#             serializer = PostSerializer(post)
#             return Response(serializer.data)
#         else:
#             posts = Post.objects.all()
#             serializer = PostSerializer(posts, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         # title = request.data.get('title')
#         # body = request.data.get('body')
#         data = request.data.copy()
#         data['owner'] = request.user.id
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             post = serializer.save()
#             return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, post_id):
#         post = get_object_or_404(Post, post_id=post_id)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, post_id):
#         post = get_object_or_404(Post, post_id=post_id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# # class CommentViewSet(viewsets.ModelViewSet):
# #     queryset = Comment.objects.all()
# #     serializer_class = CommentSerializer
# #
# #     def get_permissions(self):
# #         if self.action in ['view']:
# #             return [permissions.AllowAny]
# #         if self.action in ['create']:
# #             return [permissions.IsAuthenticated()]
# #         return []
#
# class CommentView(APIView):
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         elif self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         return []
#
#     def get(self, request, comment_id=None):
#         if comment_id is not None:
#             comment = get_object_or_404(Comment, post_id=comment_id)
#             serializer = CommentSerializer(comment)
#             return Response(serializer.data)
#         else:
#             comments = Comment.objects.all()
#             serializer = CommentSerializer(comments, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         data = request.data
#         data['owner'] = request.user.id
#         serializer = CommentSerializer(data=data)
#         if serializer.is_valid():
#             post = serializer.save()
#             return Response(CommentSerializer(post).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ReactionView(APIView):
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         elif self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         return []
#
#     def get(self, request, reaction_id=None):
#         if reaction_id is not None:
#             reaction = get_object_or_404(Reaction, post_id=reaction_id)
#             serializer = ReactionSerializer(reaction)
#             return Response(serializer.data)
#         else:
#             reactions = Reaction.objects.all()
#             serializer = ReactionSerializer(reactions, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         data = request.data
#         data['owner'] = request.user.id
#         serializer = ReactionSerializer(data=data)
#         if serializer.is_valid():
#             post = serializer.save()
#             return Response(ReactionSerializer(post).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
