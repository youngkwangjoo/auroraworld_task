from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from feedmanager.models import WebLink
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import WebLink, SharedWebLink
from django.views.decorators.http import require_http_methods


@csrf_exempt
@login_required
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



@login_required
def my_weblinks(request):
    """ ✅ 로그인한 사용자가 등록한 웹 링크 목록 반환 """
    user = request.user  # 현재 로그인한 사용자
    weblinks = WebLink.objects.filter(created_by=user).values("id", "name", "url", "category", "created_at")

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

@csrf_exempt
@login_required
def share_weblink(request):
    """ ✅ 웹 링크 공유 API """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            webLinkId = data.get("webLinkId")
            userId = data.get("userId")
            sender = request.user  # 공유한 사용자

            if not webLinkId or not userId:
                return JsonResponse({"error": "웹 링크 ID와 사용자 ID가 필요합니다."}, status=400)

            try:
                userId = int(userId)  # ✅ 정수 변환
            except ValueError:
                return JsonResponse({"error": "잘못된 사용자 ID입니다."}, status=400)

            web_link = get_object_or_404(WebLink, id=webLinkId)
            recipient = get_object_or_404(CustomUser, id=userId)

            # ✅ 디버깅 로그
            print(f"📢 [DEBUG] 공유 요청 - webLinkId: {webLinkId}, userId: {userId}, sender: {sender.username}")
            print(f"📢 [DEBUG] 공유받을 사용자: {recipient.username}, ID: {recipient.id}")

            # ✅ 이미 공유된 경우 중복 저장 방지
            if SharedWebLink.objects.filter(web_link=web_link, sender=sender, recipient=recipient).exists():
                return JsonResponse({"error": "이미 공유된 웹 링크입니다."}, status=400)

            # ✅ 공유 기록 저장
            SharedWebLink.objects.create(web_link=web_link, sender=sender, recipient=recipient)

            return JsonResponse({"message": "웹 링크가 성공적으로 공유되었습니다!"})

        except WebLink.DoesNotExist:
            return JsonResponse({"error": "웹 링크를 찾을 수 없습니다."}, status=404)

        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "사용자를 찾을 수 없습니다."}, status=404)

    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)





@login_required
def shared_links_view(request):
    """ ✅ 로그인한 사용자가 공유받은 웹 링크 목록 반환 """
    user = request.user

    # 🔍 SharedWebLink에서 recipient가 현재 로그인한 유저인지 확인
    shared_links = SharedWebLink.objects.filter(recipient=user).select_related("web_link", "sender")

    # ✅ [DEBUG] 공유받은 링크 개수 확인
    print(f"📢 [DEBUG] {user.username}의 공유받은 링크 개수: {shared_links.count()}")
    
    # ✅ [DEBUG] 공유받은 링크의 전체 데이터 확인
    print(f"📢 [DEBUG] 공유된 데이터 목록: {list(shared_links.values('web_link__name', 'web_link__url', 'sender__username', 'recipient_id'))}")

    # JSON 반환 데이터
    shared_list = [
        {
            "id": link.web_link.id,
            "name": link.web_link.name,
            "url": link.web_link.url,
            "category": link.web_link.category,
            "shared_by": link.sender.username,  # ✅ 공유한 사용자 정보 추가
        }
        for link in shared_links
    ]
    return JsonResponse({"shared_links": shared_list})


@login_required
@require_http_methods(["POST"])
def share_all_weblinks(request):
    """ ✅ 사용자의 모든 웹 링크를 특정 사용자에게 한 번에 공유 (읽기/쓰기 권한 추가) """
    try:
        data = json.loads(request.body)
        recipient_id = data.get("recipientId")
        permission = data.get("permission", "read")  # ✅ 기본값: read

        sender = request.user
        recipient = get_object_or_404(CustomUser, id=recipient_id)
        sender_weblinks = WebLink.objects.filter(created_by=sender)

        if not sender_weblinks.exists():
            return JsonResponse({"error": "공유할 웹 링크가 없습니다."}, status=400)

        shared_links = []
        for weblink in sender_weblinks:
            existing_share = SharedWebLink.objects.filter(web_link=weblink, sender=sender, recipient=recipient).first()
            if existing_share:
                existing_share.permission = permission  # ✅ 기존 공유 권한 업데이트
                existing_share.save()
            else:
                shared_link = SharedWebLink.objects.create(web_link=weblink, sender=sender, recipient=recipient, permission=permission)
                shared_links.append({
                    "name": shared_link.web_link.name,
                    "url": shared_link.web_link.url
                })

        print(f"📢 [DEBUG] 저장된 전체 공유 데이터: {shared_links}")

        return JsonResponse({"message": "✅ 모든 웹 링크가 성공적으로 공유되었습니다!", "shared_links": shared_links})

    except Exception as e:
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)

@csrf_exempt
def update_permission(request):
    """ ✅ 공유된 웹 링크의 권한을 변경하는 API """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            web_link_id = data.get("webLinkId")
            new_permission = data.get("permission")

            # ✅ 권한 값 검증
            if new_permission not in ["read", "write"]:
                return JsonResponse({"error": "잘못된 권한 값입니다."}, status=400)

            shared_link = SharedWebLink.objects.get(id=web_link_id)
            shared_link.permission = new_permission
            shared_link.save()

            return JsonResponse({"message": "권한이 성공적으로 변경되었습니다!"})

        except SharedWebLink.DoesNotExist:
            return JsonResponse({"error": "해당 웹 링크를 찾을 수 없습니다."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)

    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)