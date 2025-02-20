from django.db import models
from users.models import CustomUser  # 사용자 모델 import

class WebLink(models.Model):
    CATEGORY_CHOICES = [
        ("personal", "개인 즐겨찾기"),
        ("work", "업무 활용 자료"),
        ("reference", "참고 자료"),
        ("education", "교육 및 학습 자료"),
        ("other", "기타"),
    ]

    id = models.AutoField(primary_key=True)  # ✅ 고유한 식별자 (자동 증가)
    name = models.CharField(max_length=255)  # ✅ 웹 링크 이름
    url = models.URLField(unique=True)  # ✅ 저장할 웹 사이트 URL
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="personal")  # ✅ 카테고리 선택

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_links")  # ✅ 등록한 사람
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_links")  # ✅ 마지막 수정한 사람 (삭제 가능)

    created_at = models.DateTimeField(auto_now_add=True)  # ✅ 처음 등록한 날짜
    updated_at = models.DateTimeField(auto_now=True)  # ✅ 마지막 수정한 날짜
    deleted_at = models.DateTimeField(null=True, blank=True)  # ✅ 삭제한 날짜
    is_deleted = models.BooleanField(default=False)  # ✅ 삭제 여부 (True = 삭제됨)

    def soft_delete(self):
        """ ✅ 소프트 삭제 (삭제 날짜 기록 & is_deleted=True 설정) """
        self.is_deleted = True
        self.deleted_at = models.DateTimeField(auto_now=True)
        self.save()

    def restore(self):
        """ ✅ 삭제된 링크 복구 """
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.name} - {self.url} ({'삭제됨' if self.is_deleted else '활성'})"
