from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # AbstractUser에서 받아온 필드 중 수정하고 싶지 않은 필드 지정하기
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    # 입력받고 싶은 필드들 작성하기
    name = models.CharField(
        max_length=30,
    )
    avatar = models.URLField(
        blank=True,
    )
    birth = models.DateField(
        null=True,
    )
    phonenumber = models.CharField(
        max_length=20,
    )
    nickname = models.CharField(
        max_length=30,
        default="",
    )
    email = models.EmailField()
