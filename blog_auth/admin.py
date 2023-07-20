from django.contrib import admin

from blog_auth.models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'role']  # Fields to display in the list view
    list_filter = ['role']  # Filter options in the admin sidebar
    search_fields = ['user__username']  # Search by username


admin.site.register(Profile, ProfileAdmin)
