from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    user_id = models.IntegerField(null=True)
    age = models.IntegerField(null=True, blank=True)  # 나이 필드 추가
    birth_date = models.DateField(null=True, blank=True) # 생년월일
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 전화 번호 필드 추가
    address = models.CharField(max_length=255, blank=True, null=True)  # 주소 필드 추가
    profile_image = models.ImageField("프로필 이미지", upload_to="users/profile",
                                      blank=True)
    short_description = models.TextField('소개글', blank=True)

    def __str__(self):
        return self.username  # 사용자 이름을 기본 출력으로 설정
