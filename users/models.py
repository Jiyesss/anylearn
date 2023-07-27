from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(
        max_length=30,
        editable=False,
    )

    avatar = models.URLField(
        blank=True,
    )
    birth = models.DateField(
        null=True,
    )
    phonenumber = models.CharField(
        max_length=20,
        editable=False,
    )
    nickname = models.CharField(
        max_length=30,
        default="",
    )
    email = models.EmailField()
