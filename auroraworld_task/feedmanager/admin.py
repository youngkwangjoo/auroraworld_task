from django.contrib import admin
from .models import WebLink

@admin.register(WebLink)
class WebLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "category", "created_by", "created_at", "is_deleted")
    list_filter = ("category", "is_deleted", "created_at")
    search_fields = ("name", "url", "created_by__username")
