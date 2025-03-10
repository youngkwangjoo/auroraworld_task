import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser


def get_tokens_for_user(user):
    """
    사용자를 위한 JWT 액세스 및 리프레시 토큰 생성 함수.
    
    - `refresh`: 리프레시 토큰 (새로운 액세스 토큰을 발급받을 때 사용)
    - `access`: 액세스 토큰 (API 요청 시 인증을 위해 사용)
    - 사용자명(`username`)을 토큰에 추가하여 인증 시 활용 가능
    """
    refresh = RefreshToken.for_user(user)
    refresh["username"] = user.username  # JWT 커스텀 클레임 추가
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

@csrf_exempt  # ✅ CSRF 비활성화 (API 테스트용)
def signup_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            name = data.get("name")
            password = data.get("password")

            # ✅ 아이디 및 이메일 중복 확인
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({"error": "이미 사용 중인 아이디입니다."}, status=400)
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"error": "이미 가입된 이메일입니다."}, status=400)

            # ✅ 비밀번호 검증 (최소 길이 및 강도)
            try:
                validate_password(password)
            except ValidationError as e:
                return JsonResponse({"error": e.messages[0]}, status=400)

            # ✅ 사용자 생성 및 저장
            user = CustomUser(username=username, email=email, name=name)
            user.set_password(password)  # ✅ 비밀번호 암호화 저장
            user.save()

            return JsonResponse({"message": "회원가입이 완료되었습니다!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # ✅ GET 요청이 들어오면 signup.html 렌더링
    return render(request, "users/signup.html")

@csrf_exempt
def signin_view(request):
    """
    로그인 처리 및 JWT 액세스/리프레시 토큰을 쿠키에 저장하는 뷰.
    
    - POST 요청 시 `username`과 `password`를 이용해 사용자 인증
    - 인증 성공 시 JWT 토큰을 발급하여 `access_token`과 `refresh_token`을 HttpOnly 쿠키에 저장
    - 로그인 성공 후 `all_links_page`로 리디렉션
    - 로그인 실패 시 로그인 페이지로 다시 이동
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # 사용자 인증
        user = authenticate(request, username=username, password=password)
        if user is not None:
            tokens = get_tokens_for_user(user)

            response = redirect("all_links_page")  # 로그인 성공 시 전체 웹 링크 페이지로 이동
            response.set_cookie("access_token", tokens["access"], httponly=True, secure=True, samesite="Lax")
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=True, samesite="Lax")
            return response
        else:
            return JsonResponse({"error": "아이디 또는 비밀번호가 올바르지 않습니다."}, status=400)

    return render(request, "users/signin.html")  # GET 요청 시 로그인 페이지 렌더링


@api_view(["POST"])
def refresh_token_view(request):
    """
    리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급하는 API.
    
    - `refresh_token` 쿠키에서 리프레시 토큰을 가져와 새로운 액세스 토큰을 생성
    - 새로운 액세스 토큰을 반환하고 쿠키에 저장
    - 리프레시 토큰이 없거나 유효하지 않으면 401 오류 반환
    """
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return JsonResponse({"error": "리프레시 토큰이 없습니다."}, status=401)

    try:
        refresh = RefreshToken(refresh_token)  # 리프레시 토큰을 사용하여 새로운 액세스 토큰 발급
        new_access_token = str(refresh.access_token)

        response = JsonResponse({"access_token": new_access_token})
        response.set_cookie("access_token", new_access_token, httponly=True, secure=True, samesite="Lax")
        return response
    except Exception:
        return JsonResponse({"error": "유효하지 않은 리프레시 토큰입니다."}, status=401)


def logout_view(request):
    """
    로그아웃을 처리하는 뷰.
    
    - 사용자의 `access_token`과 `refresh_token` 쿠키를 삭제하여 로그아웃 처리
    - 로그아웃 후 로그인 페이지로 리디렉션
    """
    response = redirect("signin")  # 로그아웃 후 로그인 페이지로 이동
    response.delete_cookie("access_token")  # 액세스 토큰 삭제
    response.delete_cookie("refresh_token")  # 리프레시 토큰 삭제
    return response
