from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view
from users.models import CustomUser


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

    user_list = [
        {"id": user["id"], "username": user["username"], "name": user["name"], "email": user["email"]}
        for user in users
    ]
    return JsonResponse({"users": user_list})
