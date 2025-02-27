import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
from users.models import CustomUser


def jwt_required(view_func):
    """
    JWT 인증이 필요한 뷰에 적용하는 데코레이터.
    
    - 요청의 쿠키에서 `access_token`을 가져와 인증을 수행함.
    - 토큰이 없거나 유효하지 않으면 401 오류를 반환.
    - 인증이 성공하면 `request.user`에 해당 사용자 객체를 설정하고 원래의 뷰를 실행함.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")  # 쿠키에서 JWT 토큰 가져오기

        if not token:
            return JsonResponse({"error": "인증이 필요합니다."}, status=401)  # 토큰이 없으면 인증 오류 반환

        try:
            # JWT 토큰 디코딩 및 사용자 ID 추출
            decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            # 데이터베이스에서 사용자 조회
            request.user = CustomUser.objects.get(id=user_id)

            # 인증된 사용자가 있으면 원래의 뷰 함수 실행
            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "토큰이 만료되었습니다."}, status=401)  # 토큰 만료 시 오류 반환
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "유효하지 않은 토큰입니다."}, status=401)  # 토큰이 유효하지 않으면 오류 반환

    return wrapper
