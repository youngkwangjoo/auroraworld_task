from django.urls import path
from .views import add_weblink, my_weblinks, all_links_view, edit_weblink, delete_weblink, share_weblink, shared_links_view, share_all_weblinks, update_permission, get_shared_weblink, edit_shared_weblink

urlpatterns = [
    path("add/", add_weblink, name="add_weblink"),
    path("all_links/", my_weblinks, name="my_weblinks"),  
    path("all_links_page/", all_links_view, name="all_links_page"), 
    path("edit/<int:pk>/", edit_weblink, name="edit_weblink"),
    path("delete/<int:pk>/", delete_weblink, name="delete_weblink"),
    path("share/", share_weblink, name="share_weblink"), 
    path("shared_links/", shared_links_view, name="shared_links"),
    path("share_all/", share_all_weblinks, name="share_all_weblinks"),
    path("update_permission/", update_permission, name="update_permission"),
    path("shared_link/<int:web_link_id>/", get_shared_weblink, name="get_shared_weblink"),  
    path("update_shared_link/<int:web_link_id>/", edit_shared_weblink, name="edit_shared_weblink"), 
]
