from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser

# ✅ 사용자 추가를 위한 커스텀 폼 (비밀번호 해싱 포함)
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "name", "password", "is_staff", "is_active")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # ✅ 비밀번호 해싱
        if commit:
            user.save()
        return user


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # ✅ Admin에서 보이는 필드 설정
    list_display = ("id", "username", "name", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "name", "email")
    ordering = ("id",)

    # ✅ 사용자 추가 시 사용할 폼 설정
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "name", "password", "is_staff", "is_active"),
        }),
    )

    # ✅ 사용자 수정 시 기본 제공되는 필드 설정
    fieldsets = (
        (None, {"fields": ("username", "email", "name", "password")}),
        ("권한 설정", {"fields": ("is_staff", "is_active")}),
    )
