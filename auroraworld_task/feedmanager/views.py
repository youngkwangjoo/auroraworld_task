import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from feedmanager.models import WebLink
from users.models import CustomUser
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import WebLink, SharedWebLink
from django.views.decorators.http import require_http_methods
from users.views.decorators import jwt_required 

# 사용자가 웹 링크를 추가할 수 있도록 처리하는 함수, 나의웹링크 - 등록
@csrf_exempt
@jwt_required
def add_weblink(request):
    """ ✅ 웹 링크 등록 API """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get("url")
            name = data.get("name")
            category = data.get("category", "personal")  # 기본 카테고리 설정
            user = request.user  # 로그인한 사용자

            # 필수 입력값 확인
            if not url or not name:
                return JsonResponse({"error": "웹 링크와 이름을 입력하세요."}, status=400)

            # ✅ 기존에 같은 사용자가 동일한 URL을 등록했는지 확인
            if WebLink.objects.filter(url=url, created_by=user).exists():
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


#사용자가 등록한 웹링크 목록을 반환하는 함수, json 데이터를 반환
@jwt_required
def my_weblinks(request):
    user = request.user  # 현재 로그인한 사용자
    weblinks = WebLink.objects.filter(created_by=user).values("id", "name", "url", "category", "created_at")

    return JsonResponse({"weblinks": list(weblinks)})

# html페이지에 웹링크를 랜더링 하는데 사용하는 함수 
@jwt_required
def all_links_view(request):
    return render(request, "all_links.html", {"username": request.user.username})

# 웹링크를 수정하는 함수
@csrf_exempt
@jwt_required
def edit_weblink(request, pk):  
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

# 웹링크를 삭제하는 함수, db에서 완전삭제
@jwt_required
def delete_weblink(request, pk):
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE 요청만 허용됩니다."}, status=405)

    try:
        weblink = get_object_or_404(WebLink, id=pk)
        weblink.delete()
        return JsonResponse({"message": "웹 링크가 삭제되었습니다!"})

    except Exception as e:
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)

# 웹링크를 공유하는 함수, 특정 사용자에게 공유, 기본값은 읽기권한
@csrf_exempt
@jwt_required
def share_weblink(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            webLinkId = data.get("webLinkId")
            userId = data.get("userId")
            permission = data.get("permission", "read") 
            sender = request.user

            web_link = get_object_or_404(WebLink, id=webLinkId, created_by=sender)
            recipient = get_object_or_404(CustomUser, id=userId)

            shared_link, created = SharedWebLink.objects.update_or_create(
                web_link=web_link,
                recipient=recipient,
                defaults={"sender": sender, "permission": permission}
            )

            return JsonResponse({"message": "웹 링크가 공유되었습니다!", "permission": shared_link.permission})

        except (WebLink.DoesNotExist, CustomUser.DoesNotExist):
            return JsonResponse({"error": "웹 링크 또는 사용자를 찾을 수 없습니다."}, status=404)

    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)

# 공유받은 웹 링크 목록을 반환하는 함수
@jwt_required
def shared_links_view(request):
    user = request.user
    shared_links = SharedWebLink.objects.filter(recipient=user).select_related("web_link", "sender")

    shared_list = [
        {
            "id": link.web_link.id,
            "name": link.web_link.name,
            "url": link.web_link.url,
            "category": link.web_link.category,
            "shared_by": link.sender.username,
            "permission": link.permission,
        }
        for link in shared_links
    ]
    return JsonResponse({"shared_links": shared_list})

# 전체 웹링크를 한번에 공유하는 함수
@jwt_required
def edit_shared_weblink(request, web_link_id):
    if request.method == "PUT":
        shared_link = get_object_or_404(SharedWebLink, web_link_id=web_link_id, recipient=request.user)


        if shared_link.permission != "write":
            return JsonResponse({"error": "❌ 수정 권한이 없습니다!"}, status=403)

        try:
            data = json.loads(request.body)
            web_link = shared_link.web_link 
            web_link.name = data["name"]
            web_link.url = data["url"]
            web_link.save()
            
            return JsonResponse({"message": "✅ 공유받은 웹 링크가 수정되었습니다!"})

        except Exception as e:
            return JsonResponse({"error": f"❌ 수정 중 오류 발생: {str(e)}"}, status=500)

    return JsonResponse({"error": "❌ PUT 요청만 허용됩니다."}, status=405)

# 공유된 웹링킁
@jwt_required
@require_http_methods(["POST"])
def share_all_weblinks(request):
    try:
        data = json.loads(request.body)
        recipient_id = data.get("recipientId")
        permission = data.get("permission", "read")

        sender = request.user
        recipient = get_object_or_404(CustomUser, id=recipient_id)
        sender_weblinks = WebLink.objects.filter(created_by=sender)

        if not sender_weblinks.exists():
            return JsonResponse({"error": "공유할 웹 링크가 없습니다."}, status=400)

        for weblink in sender_weblinks:
            SharedWebLink.objects.update_or_create(
                web_link=weblink,
                recipient=recipient,
                defaults={"sender": sender, "permission": permission}
            )

        return JsonResponse({"message": "✅ 모든 웹 링크가 성공적으로 공유되었습니다!"})

    except Exception as e:
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)

#이미 공유한 웹링크를 수정해서 공유업데이트 할때 사용하는 함수
@csrf_exempt
@jwt_required
def update_permission(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            web_link_id = data.get("webLinkId")
            new_permission = data.get("permission")

            if new_permission not in ["read", "write"]:
                return JsonResponse({"error": "잘못된 권한 값입니다."}, status=400)

            shared_link = get_object_or_404(SharedWebLink, id=web_link_id)
            shared_link.permission = new_permission
            shared_link.save()

            return JsonResponse({"message": "권한이 변경되었습니다!"})

        except SharedWebLink.DoesNotExist:
            return JsonResponse({"error": "해당 웹 링크를 찾을 수 없습니다."}, status=404)

    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)

#공유받은 웹 링크 중 하나의 정보를 조회하는 함수
@jwt_required
def get_shared_weblink(request, web_link_id):
    shared_link = get_object_or_404(SharedWebLink, web_link__id=web_link_id, recipient=request.user)

    return JsonResponse({
        "id": shared_link.web_link.id,
        "name": shared_link.web_link.name,
        "url": shared_link.web_link.url,
        "category": shared_link.web_link.category,
        "shared_by": shared_link.sender.username,
        "permission": shared_link.permission,
    })
