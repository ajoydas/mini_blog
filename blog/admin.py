from django.contrib import admin

from blog.models import Post, Comment, Reaction

"""
This file registers Post, Comment and Reaction models with the admin site.
"""


class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'created_at', 'updated_at']
    list_filter = ['owner']
    search_fields = ['owner__username', 'title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'post', 'created_at', 'updated_at']
    list_filter = ['owner', 'post']
    search_fields = ['owner__username', 'post__title',
                     'body']


class ReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'reaction_type', 'timestamp']
    list_filter = ['user', 'reaction_type']
    search_fields = ['user__username']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reaction, ReactionAdmin)
