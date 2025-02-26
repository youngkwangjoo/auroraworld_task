import jwt
import json
from django.db.models import Q  # ✅ Q 객체 import
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser  # ✅ 중복 import 정리
from feedmanager.models import WebLink
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

def logout_view(request):
    """ ✅ 로그아웃 시 JWT 블랙리스트에 추가 후 삭제 """
    refresh_token = request.COOKIES.get("refresh_token")
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            BlacklistedToken.objects.get_or_create(token=token)
        except Exception as e:
            print(f"🔴 블랙리스트 등록 실패: {e}")

    response = redirect("signin")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response



def get_tokens_for_user(user):
    """ ✅ JWT 액세스 및 리프레시 토큰 생성 (username 포함) """
    refresh = RefreshToken.for_user(user)

    # ✅ 커스텀 클레임 추가
    refresh["username"] = user.username  

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
            # ✅ JWT 토큰 생성 (username 포함)
            tokens = get_tokens_for_user(user)

            response = redirect("auroramain")

            # ✅ JWT 토큰을 HttpOnly 쿠키에 저장
            response.set_cookie("access_token", tokens["access"], httponly=True, secure=True, samesite="Lax")
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=True, samesite="Lax")

            return response
        else:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
            return redirect("signin")

    return render(request, "users/signin.html")



@api_view(["GET"])
def protected_view(request):
    """ ✅ JWT 쿠키 인증이 필요한 보호된 API """
    token = request.COOKIES.get("access_token")
    if not token:
        return JsonResponse({"error": "인증이 필요합니다."}, status=401)

    try:
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        user = CustomUser.objects.get(id=user_id)
        return JsonResponse({"message": "인증 성공!", "username": user.username})
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "토큰이 만료되었습니다."}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "유효하지 않은 토큰입니다."}, status=401)



def auroramain_view(request):
    """ ✅ Aurora Main 페이지 (JWT 토큰 없으면 로그인 페이지로 이동) """
    token = request.COOKIES.get("access_token")

    if not token:
        return redirect("signin")

    try:
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        user = CustomUser.objects.get(id=user_id)
        return render(request, "auroramain.html", {"username": user.username})
    except jwt.ExpiredSignatureError:
        return redirect("signin")
    except jwt.InvalidTokenError:
        return redirect("signin")


@api_view(["GET"])
def search_users(request):
    """ ✅ 사용자 검색 API (username 기본 검색, name 및 email도 가능) """
    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse({"users": []})

    users = CustomUser.objects.filter(
        Q(username__icontains=query) |
        Q(name__icontains=query) |
        Q(email__icontains=query)
    ).values("id", "username", "name", "email")

    return JsonResponse({"users": list(users)})

@api_view(["GET"])
def all_users(request):
    """ ✅ 사용자 목록을 JSON 형식으로 반환 """
    users = CustomUser.objects.values("id", "username", "name", "email")
    
    # ✅ 디버깅용 출력
    print("🔹 사용자 목록:", list(users)) 

    user_list = [
        {"id": user["id"], "username": user["username"], "name": user["name"], "email": user["email"]}
        for user in users
    ]
    return JsonResponse({"users": user_list})

@api_view(["POST"])
def refresh_token_view(request):
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
    """ ✅ 로그아웃 시 JWT 블랙리스트에 추가 후 삭제 """
    refresh_token = request.COOKIES.get("refresh_token")
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ 블랙리스트 등록
        except Exception as e:
            print(f"🔴 블랙리스트 등록 실패: {e}")

    response = redirect("signin")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
