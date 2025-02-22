from django.urls import path
from .views import add_weblink, my_weblinks, all_links_view, edit_weblink, delete_weblink, share_weblink, shared_links_view

urlpatterns = [
    path("add/", add_weblink, name="add_weblink"),
    path("all_links/", my_weblinks, name="my_weblinks"),  
    path("all_links_page/", all_links_view, name="all_links_page"), 
    path("edit/<int:pk>/", edit_weblink, name="edit_weblink"),
    path("delete/<int:pk>/", delete_weblink, name="delete_weblink"),
    path("share/", share_weblink, name="share_weblink"), 
    path("shared_links/", shared_links_view, name="shared_links"),
]
