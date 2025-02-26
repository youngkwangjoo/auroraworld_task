from django.urls import path
from users.views.login import signup_view, signin_view, logout_view, refresh_token_view
from users.views.search import search_users, all_users
from users.views.auth import auroramain_view, protected_view  # ✅ JWT 인증 관련 추가

urlpatterns = [
    path("signup/", signup_view, name="signup"),  # 회원가입
    path("signin/", signin_view, name="signin"),  # 로그인
    path("logout/", logout_view, name="logout"),  # 로그아웃
    path("refresh/", refresh_token_view, name="refresh_token_view"),  # ✅ 토큰 갱신

    path("auroramain/", auroramain_view, name="auroramain"),  # ✅ Aurora Main 페이지 (JWT 검증)
    path("protected/", protected_view, name="protected"),  # ✅ JWT 인증이 필요한 API

    path("search/", search_users, name="search_users"),  # ✅ 사용자 검색
    path("all_users/", all_users, name="all_users"),  # ✅ 전체 사용자 조회
]
