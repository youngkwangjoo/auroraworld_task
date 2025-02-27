from django.urls import path
from .views import (
    add_weblink, my_weblinks, all_links_view, edit_weblink, delete_weblink, 
    share_weblink, shared_links_view, share_all_weblinks, update_permission, 
    get_shared_weblink, edit_shared_weblink
)

urlpatterns = [
    path("add/", add_weblink, name="add_weblink"),  
    # 새로운 웹 링크를 추가하는 API

    path("all_links/", my_weblinks, name="my_weblinks"),  
    # 현재 로그인한 사용자의 웹 링크 목록을 가져오는 API (JSON 응답)

    path("all_links_page/", all_links_view, name="all_links_page"),  
    # 모든 웹 링크 목록을 HTML 페이지로 렌더링하는 뷰

    path("edit/<int:pk>/", edit_weblink, name="edit_weblink"),  
    # 특정 웹 링크 정보를 수정하는 API (웹 링크 ID를 기반으로 수정)

    path("delete/<int:pk>/", delete_weblink, name="delete_weblink"),  
    # 특정 웹 링크를 삭제하는 API (웹 링크 ID를 기반으로 삭제)

    path("share/", share_weblink, name="share_weblink"),  
    # 특정 웹 링크를 다른 사용자에게 공유하는 API

    path("shared_links/", shared_links_view, name="shared_links"),  
    # 공유받은 웹 링크 목록을 가져오는 API

    path("share_all/", share_all_weblinks, name="share_all_weblinks"),  
    # 사용자가 자신의 모든 웹 링크를 특정 사용자와 공유하는 API

    path("update_permission/", update_permission, name="update_permission"),  
    # 공유된 웹 링크의 읽기/쓰기 권한을 수정하는 API

    path("shared_link/<int:web_link_id>/", get_shared_weblink, name="get_shared_weblink"),  
    # 공유된 특정 웹 링크 정보를 조회하는 API (웹 링크 ID 기반)

    path("update_shared_link/<int:web_link_id>/", edit_shared_weblink, name="edit_shared_weblink"),  
    # 공유된 특정 웹 링크 정보를 수정하는 API (쓰기 권한이 있을 경우 가능)
]
