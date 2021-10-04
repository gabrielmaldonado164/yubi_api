"""User models admin"""

#Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from yubi.users.models.users import User
from yubi.users.models.profiles import Profile

class CustomUserAdmin(UserAdmin):
    """User models admin"""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client')
    list_filter = ['is_client', 'is_staff', 'date_created', 'date_modified']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile models admin."""
    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ['reputation']

admin.site.register(User, CustomUserAdmin)

