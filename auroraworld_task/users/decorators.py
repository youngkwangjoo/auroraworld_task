import jwt
from django.http import JsonResponse
from django.conf import settings
from users.models import CustomUser
from functools import wraps

def jwt_required(view_func):
    """ ✅ JWT 인증 데코레이터 (request.user 설정) """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            return JsonResponse({"error": "인증이 필요합니다."}, status=401)

        try:
            decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
            request.user = CustomUser.objects.get(id=user_id)  # ✅ request.user 직접 설정
            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "토큰이 만료되었습니다."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "유효하지 않은 토큰입니다."}, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "사용자를 찾을 수 없습니다."}, status=404)

    return _wrapped_view
