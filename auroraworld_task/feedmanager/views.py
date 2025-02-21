from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from feedmanager.models import WebLink
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import WebLink


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
def all_links_view(request):
    """ ✅ 전체 웹 링크 목록 페이지 렌더링 """
    return render(request, "all_links.html", {"username": request.user.username})


@csrf_exempt
@login_required
def edit_weblink(request, pk):  # pk 인자 추가
    """ 웹 링크 수정 API """
    if request.method != "PUT":
        return JsonResponse({"error": "PUT 요청만 허용됩니다."}, status=405)

    try:
        # JSON 데이터 파싱
        data = json.loads(request.body)

        # 웹 링크 객체 찾기 (pk로 검색)
        weblink = get_object_or_404(WebLink, id=pk)

        # 값 업데이트
        weblink.name = data.get("name", weblink.name)
        weblink.url = data.get("url", weblink.url)
        weblink.save()

        return JsonResponse({"message": "수정 완료", "name": weblink.name, "url": weblink.url})

    except json.JSONDecodeError:
        return JsonResponse({"error": "올바른 JSON 형식이 아닙니다."}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)

@csrf_exempt
def delete_weblink(request, pk):
    """ ✅ DB에서 완전히 삭제하는 웹 링크 삭제 API """
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE 요청만 허용됩니다."}, status=405)

    try:
        weblink = get_object_or_404(WebLink, id=pk)
        weblink.delete()  # ✅ DB에서 완전히 삭제!
        return JsonResponse({"message": "웹 링크가 삭제되었습니다!"})

    except Exception as e:
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)
