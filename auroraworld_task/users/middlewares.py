import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from users.models import CustomUser
from django.http import JsonResponse

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """ ✅ 모든 요청에서 JWT를 자동으로 인증하는 미들웨어 """
    def process_request(self, request):
        token = request.COOKIES.get("access_token")
        if token:
            try:
                decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
                user_id = decoded_token.get("user_id")
                user = CustomUser.objects.get(id=user_id)
                request.user = user  # ✅ request.user에 인증된 사용자 정보 추가
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "토큰이 만료되었습니다."}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "유효하지 않은 토큰입니다."}, status=401)
        else:
            request.user = None  # 인증되지 않은 사용자
