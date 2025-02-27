import jwt
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from users.models import CustomUser
from rest_framework.decorators import api_view


def auroramain_view(request):
    """
    Aurora Main 페이지를 렌더링하는 뷰 함수.
    
    - 사용자의 JWT 토큰을 쿠키에서 가져와 인증을 확인함.
    - 토큰이 없거나 유효하지 않으면 로그인 페이지(signin)로 리디렉션.
    - 유효한 경우, 사용자 정보를 조회하여 auroramain.html을 렌더링.
    """
    token = request.COOKIES.get("access_token")  # 쿠키에서 JWT 토큰 가져오기

    if not token:
        return redirect("signin")  # 토큰이 없으면 로그인 페이지로 이동

    try:
        # JWT 토큰 디코딩 및 사용자 조회
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        user = CustomUser.objects.get(id=user_id)

        # 사용자명을 템플릿에 전달하여 렌더링
        return render(request, "auroramain.html", {"username": user.username})

    except jwt.ExpiredSignatureError:
        return redirect("signin")  # 토큰이 만료되었으면 로그인 페이지로 이동
    except jwt.InvalidTokenError:
        return redirect("signin")  # 토큰이 유효하지 않으면 로그인 페이지로 이동


@api_view(["GET"])
def protected_view(request):
    """
    인증이 필요한 보호된 API 엔드포인트.
    
    - JWT 토큰을 쿠키에서 가져와 유효성을 검사.
    - 토큰이 없거나 유효하지 않으면 401 오류 반환.
    - 인증 성공 시, 사용자명을 포함한 JSON 응답 반환.
    """
    token = request.COOKIES.get("access_token")  # 쿠키에서 JWT 토큰 가져오기

    if not token:
        return JsonResponse({"error": "인증이 필요합니다."}, status=401)  # 토큰이 없으면 인증 오류 반환

    try:
        # JWT 토큰 디코딩 및 사용자 조회
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        user = CustomUser.objects.get(id=user_id)

        return JsonResponse({"message": "인증 성공!", "username": user.username})  # 인증 성공 응답

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "토큰이 만료되었습니다."}, status=401)  # 토큰 만료 시 오류 반환
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "유효하지 않은 토큰입니다."}, status=401)  # 토큰이 유효하지 않으면 오류 반환
