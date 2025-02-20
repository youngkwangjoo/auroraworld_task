import jwt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt 

def get_tokens_for_user(user):
    """ JWT 액세스 및 리프레시 토큰 생성 """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def signup_view(request):
    """ 회원가입 뷰 """
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
    """ 로그인 + JWT 토큰을 HttpOnly 쿠키에 저장 후 auroramain.html로 이동 """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # JWT 토큰 생성
            tokens = get_tokens_for_user(user)

            response = redirect("auroramain")  # ✅ 로그인 성공 시 auroramain.html로 이동

            # JWT 토큰을 HttpOnly 쿠키에 저장
            response.set_cookie("access_token", tokens["access"], httponly=True, secure=True, samesite="Lax")
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=True, samesite="Lax")

            return response
        else:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
            return redirect("signin")

    return render(request, "users/signin.html")


@api_view(["GET"])
def protected_view(request):
    """ JWT 쿠키 인증이 필요한 보호된 API """
    token = request.COOKIES.get("access_token")
    if not token:
        return JsonResponse({"error": "인증이 필요합니다."}, status=401)

    try:
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
        return JsonResponse({"message": "인증 성공!", "username": decoded_token["username"]})
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "토큰이 만료되었습니다."}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "유효하지 않은 토큰입니다."}, status=401)


def logout_view(request):
    """ 로그아웃 시 JWT 쿠키 삭제 후 로그인 페이지로 이동 """
    response = redirect("signin")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response



def auroramain_view(request):
    """ Aurora Main 페이지 (쿠키에 JWT 토큰이 없으면 로그인 페이지로 이동) """
    token = request.COOKIES.get("access_token")

    if not token:
        return redirect("signin")  # ✅ JWT 없으면 로그인 페이지로 이동

    try:
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
        user_id = decoded_token.get("user_id")  # ✅ JWT에서 user_id 가져오기
        user = CustomUser.objects.get(id=user_id)  # ✅ user_id로 CustomUser 모델에서 username 가져오기
        return render(request, "auroramain.html", {"username": user.username})  # ✅ 템플릿에 username 전달
    except jwt.ExpiredSignatureError:
        return redirect("signin")  # ✅ 토큰 만료 시 로그인 페이지로 이동
    except jwt.InvalidTokenError:
        return redirect("signin")  # ✅ 유효하지 않은 토큰이면 로그인 페이지로 이동

def search_users(request):
    """ 전체 사용자 목록을 JSON으로 반환 """
    users = CustomUser.objects.all().values("id", "username", "email", "name")
    return JsonResponse({"users": list(users)})
