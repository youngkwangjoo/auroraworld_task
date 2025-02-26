import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
from users.models import CustomUser


def jwt_required(view_func):
    """ ✅ JWT 토큰이 필요함 """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            return JsonResponse({"error": "인증이 필요합니다."}, status=401)

        try:
            decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
            request.user = CustomUser.objects.get(id=user_id)
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "토큰이 만료되었습니다."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "유효하지 않은 토큰입니다."}, status=401)

    return wrapper
