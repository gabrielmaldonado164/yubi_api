"""Box admin"""

# Django
from django.contrib import admin

#Models 
from yubi.boxes.models.box import Box

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'slug_name',
        'name',
        'is_public',
        'is_limited',
        'is_verified',
        'member_limited'
    )

    search_fields = ('slug_name', 'name')
    list_filter = (
        'is_public',
        'is_verified',
        'is_limited'
    )