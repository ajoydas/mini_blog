from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.views.comment import CommentView, CommentListView
from blog.views.post import PostView
from blog.views.reaction import ReactionView

router = DefaultRouter()
# router.register(r'posts', PostViewSet)
# router.register(r'comments', CommentViewSet)
# router.register(r'reactions', ReactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts', PostView.as_view(), name='post-list'),
    path('posts/<int:post_id>', PostView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments', CommentListView.as_view(), name='post-comments'),
    # path('comments', CommentView.as_view(), name='comment-list'),
    path('comments', CommentView.as_view(), name='comment-route'),
    path('comments/<int:comment_id>', CommentView.as_view(), name='comment-detail'),
    path('comments/<int:comment_id>/replies', CommentListView().as_view(), name='comment-replies'),
    path('posts/<int:post_id>/reactions', ReactionView.as_view(), name='post-reaction'),
    path('posts/<int:post_id>/reactions/<str:reaction_type>', ReactionView.as_view(), name='post-reaction-interact'),
    path('comments/<int:comment_id>/reactions', ReactionView.as_view(), name='comment-reaction'),
    path('comments/<int:comment_id>/reactions/<str:reaction_type>', ReactionView.as_view(),
         name='comment-reaction-interact'),
]
