import jwt
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.views.decorators.csrf import csrf_exempt


def get_tokens_for_user(user):
    """ ✅ JWT 액세스 및 리프레시 토큰 생성 (username 포함) """
    refresh = RefreshToken.for_user(user)
    refresh["username"] = user.username  # ✅ JWT 커스텀 클레임 추가
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def signup_view(request):
    """ ✅ 회원가입 뷰 """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "이미 사용 중인 아이디입니다.")
            return redirect("signup")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "이미 가입된 이메일입니다.")
            return redirect("signup")

        user = CustomUser(username=username, email=email, name=name, password=make_password(password))
        user.save()
        messages.success(request, "회원가입이 완료되었습니다. 로그인하세요.")
        return redirect("signin")

    return render(request, "users/signup.html")


@csrf_exempt
def signin_view(request):
    """ ✅ 로그인 + JWT 토큰을 HttpOnly 쿠키에 저장 후 auroramain.html로 이동 """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            tokens = get_tokens_for_user(user)

            response = redirect("all_links_page")
            response.set_cookie("access_token", tokens["access"], httponly=True, secure=True, samesite="Lax")
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=True, samesite="Lax")
            return response
        else:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
            return redirect("signin")

    return render(request, "users/signin.html")


@api_view(["POST"])
def refresh_token_view(request):
    """ ✅ 리프레시 토큰을 사용하여 새로운 액세스 토큰 발급 """
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return JsonResponse({"error": "리프레시 토큰이 없습니다."}, status=401)

    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)

        response = JsonResponse({"access_token": new_access_token})
        response.set_cookie("access_token", new_access_token, httponly=True, secure=True, samesite="Lax")
        return response
    except Exception as e:
        return JsonResponse({"error": "유효하지 않은 리프레시 토큰입니다."}, status=401)


def logout_view(request):
    """ ✅ 로그아웃 시 쿠키 삭제 """
    response = redirect("signin")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
