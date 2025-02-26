import jwt
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from users.models import CustomUser
from rest_framework.decorators import api_view


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
