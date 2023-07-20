from django.contrib import admin

from blog_auth.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin class for Profile model.
    """
    list_display = ['user', 'bio', 'role']
    list_filter = ['role']
    search_fields = ['user__username']


admin.site.register(Profile, ProfileAdmin)
