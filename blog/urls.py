from django.urls import path

from blog.views.comment import CommentView, CommentListView
from blog.views.post import PostView
from blog.views.reaction import ReactionView

urlpatterns = [
    # urls to interact with blog posts
    path('posts', PostView.as_view(), name='post-list'),
    path('posts/<int:post_id>', PostView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments', CommentListView.as_view(), name='post-comments'),

    # urls to interact with comments
    path('comments', CommentView.as_view(), name='comment-route'),
    path('comments/<int:comment_id>', CommentView.as_view(), name='comment-detail'),
    path('comments/<int:comment_id>/replies', CommentListView().as_view(), name='comment-replies'),

    # urls to interact with reactions
    path('posts/<int:post_id>/reactions', ReactionView.as_view(), name='post-reaction'),
    path('posts/<int:post_id>/reactions/<str:reaction_type>', ReactionView.as_view(), name='post-reaction-interact'),
    path('comments/<int:comment_id>/reactions', ReactionView.as_view(), name='comment-reaction'),
    path('comments/<int:comment_id>/reactions/<str:reaction_type>', ReactionView.as_view(),
         name='comment-reaction-interact'),
]
