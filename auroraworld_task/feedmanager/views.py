from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from feedmanager.models import WebLink
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@csrf_exempt
@login_required
def add_weblink(request):
    """ ✅ 웹 링크 등록 API """
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            url = data.get("url")
            name = data.get("name")
            category = data.get("category", "personal")  # 기본 카테고리 설정
            user = request.user  # 로그인한 사용자

            # 필수 입력값 확인
            if not url or not name:
                return JsonResponse({"error": "웹 링크와 이름을 입력하세요."}, status=400)

            # 기존에 같은 URL이 있는지 확인
            if WebLink.objects.filter(url=url, is_deleted=False).exists():
                return JsonResponse({"error": "이미 등록된 웹 링크입니다."}, status=400)

            # 새 웹 링크 저장
            weblink = WebLink.objects.create(
                name=name,
                url=url,
                category=category,
                created_by=user
            )

            return JsonResponse({
                "message": "웹 링크가 등록되었습니다!",
                "id": weblink.id,
                "name": weblink.name,
                "url": weblink.url,
                "category": weblink.category
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)

    return JsonResponse({"error": "POST 요청만 지원됩니다."}, status=405)


@login_required
def my_weblinks(request):
    """ ✅ 로그인한 사용자가 등록한 웹 링크 목록 반환 """
    user = request.user  # 현재 로그인한 사용자
    weblinks = WebLink.objects.filter(created_by=user, is_deleted=False).values("id", "name", "url", "category", "created_at")

    return JsonResponse({"weblinks": list(weblinks)})

@login_required
def my_links_page(request):
    """ ✅ 내 웹 링크 목록 페이지 렌더링 """
    return render(request, "all_links.html", {"username": request.user.username})