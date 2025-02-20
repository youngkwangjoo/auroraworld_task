from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일 필수 및 중복 불가
    name = models.CharField(max_length=50)  # 사용자 이름 추가
    username = models.CharField(max_length=30, unique=True)  # 아이디 (Django 기본 username 사용)

    # ✅ 공유 사용자 목록 (ManyToManyField)
    share_users = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="shared_with")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return self.username
