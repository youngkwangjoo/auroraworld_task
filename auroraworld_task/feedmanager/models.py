from django.db import models
from users.models import CustomUser  # 사용자 모델 import

class WebLink(models.Model):
    """ ✅ 웹 링크 모델 """
    CATEGORY_CHOICES = [
        ("personal", "개인 즐겨찾기"),
        ("work", "업무 활용 자료"),
        ("reference", "참고 자료"),
        ("education", "교육 및 학습 자료"),
        ("other", "기타"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="personal")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_links")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_links")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.url}"

class SharedWebLink(models.Model):
    """ ✅ 웹 링크 공유 모델 """
    web_link = models.ForeignKey(WebLink, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name="sent_links", on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name="received_links", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # ✅ 읽기 / 쓰기 권한 필드 추가
    permission = models.CharField(max_length=10, choices=[("read", "읽기"), ("write", "쓰기")], default="read")

    class Meta:
        unique_together = ("web_link", "recipient")  # 🔥 동일한 웹 링크 중복 공유 방지

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.web_link.name} ({self.permission})"
