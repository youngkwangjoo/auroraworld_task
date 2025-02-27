from django.contrib import admin
from .models import WebLink

class WebLinkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", "category", "created_by", "created_at")  
    list_filter = ("category", ) 
    search_fields = ("name", "url", "created_by__username")  

admin.site.register(WebLink, WebLinkAdmin)
