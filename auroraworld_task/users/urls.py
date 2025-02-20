from django.urls import path
from .views import signup_view, signin_view, logout_view, protected_view, auroramain_view, search_users

urlpatterns = [
    path("signup/", signup_view, name="signup"),  # 회원가입
    path("signin/", signin_view, name="signin"),  # 로그인
    path("logout/", logout_view, name="logout"),  # 로그아웃
    path("protected/", protected_view, name="protected"),  # JWT 인증이 필요한 API
    path("auroramain/", auroramain_view, name="auroramain"),  # Aurora Main 페이지
    path("search/", search_users, name="search_users"),  # ✅ 친구 찾기 API 추가
]
