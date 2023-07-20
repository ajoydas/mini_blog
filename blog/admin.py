from django.contrib import admin

from blog.models import Post, Comment, Reaction


class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'created_at', 'updated_at']  # Fields to display in the list view
    list_filter = ['owner']  # Filter options in the admin sidebar
    search_fields = ['owner__username', 'title']  # Search by owner's username or post title


class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'post', 'created_at', 'updated_at']  # Fields to display in the list view
    list_filter = ['owner', 'post']  # Filter options in the admin sidebar
    search_fields = ['owner__username', 'post__title',
                     'body']  # Search by owner's username, post title, or comment body


class ReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'reaction_type', 'timestamp']  # Fields to display in the list view
    list_filter = ['user', 'reaction_type']  # Filter options in the admin sidebar
    search_fields = ['user__username']  # Search by user's username


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reaction, ReactionAdmin)
