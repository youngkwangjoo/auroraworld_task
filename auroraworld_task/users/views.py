from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse




def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "이미 사용 중인 아이디입니다.")
            return redirect("register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "이미 가입된 이메일입니다.")
            return redirect("register")

        user = CustomUser(username=username, email=email, name=name, password=make_password(password))
        user.save()
        messages.success(request, "회원가입이 완료되었습니다. 로그인하세요.")
        return redirect("login")

    return render(request, "users/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
            return redirect("login")

    return render(request, "users/signin.html")


def logout_view(request):
    logout(request)
    return redirect("login")

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .models import CustomUser

def get_tokens_for_user(user):
    """ 사용자에 대한 JWT 액세스 및 리프레시 토큰 생성 """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

def signin_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # JWT 토큰 생성
            tokens = get_tokens_for_user(user)

            return JsonResponse({
                "message": "로그인 성공!",
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.name
                }
            })
        else:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
            return redirect("signin")

    return render(request, "users/signin.html")
