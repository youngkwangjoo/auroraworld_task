from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일 필수 및 중복 불가
    name = models.CharField(max_length=50)  # 사용자 이름 추가
    username = models.CharField(max_length=30, unique=True)  # 아이디 (Django 기본 username 사용)

    USERNAME_FIELD = "username"  # 기본 로그인 필드를 email로 설정
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return self.email
