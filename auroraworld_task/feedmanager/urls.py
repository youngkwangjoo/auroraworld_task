from django.urls import path
from .views import add_weblink, my_weblinks, my_links_page

urlpatterns = [
    path("add/", add_weblink, name="add_weblink"), 
    path("all_links/", my_weblinks, name="my_weblinks"),
    path("my_links_page/", my_links_page, name="my_links_page"),
]
