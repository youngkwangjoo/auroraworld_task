from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view
from users.models import CustomUser


@api_view(["GET"])
def search_users(request):
    """
    사용자 검색 API

    - `query` 파라미터를 이용하여 사용자 검색
    - `username`, `name`, `email`을 기준으로 검색 가능
    - 검색어가 포함된 사용자 목록을 반환
    
    요청 예시:
    ```
    GET /users/search_users/?query=john
    ```
    
    응답 예시:
    ```json
    {
        "users": [
            {"id": 1, "username": "john_doe", "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "username": "johnsmith", "name": "John Smith", "email": "johnsmith@example.com"}
        ]
    }
    ```
    """
    query = request.GET.get("query", "").strip()  # 검색어 가져오기

    # 검색어가 없으면 빈 리스트 반환
    if not query:
        return JsonResponse({"users": []})

    # username, name, email 중 검색어가 포함된 사용자 조회
    users = CustomUser.objects.filter(
        Q(username__icontains=query) |
        Q(name__icontains=query) |
        Q(email__icontains=query)
    ).values("id", "username", "name", "email")

    return JsonResponse({"users": list(users)})


@api_view(["GET"])
def all_users(request):
    """
    전체 사용자 목록을 JSON 형식으로 반환하는 API

    - 모든 사용자의 `id`, `username`, `name`, `email`을 포함한 리스트 반환

    요청 예시:
    ```
    GET /users/all_users/
    ```

    응답 예시:
    ```json
    {
        "users": [
            {"id": 1, "username": "alice", "name": "Alice Smith", "email": "alice@example.com"},
            {"id": 2, "username": "bob", "name": "Bob Johnson", "email": "bob@example.com"}
        ]
    }
    ```
    """
    users = CustomUser.objects.values("id", "username", "name", "email")

    user_list = [
        {"id": user["id"], "username": user["username"], "name": user["name"], "email": user["email"]}
        for user in users
    ]
    
    return JsonResponse({"users": user_list})
