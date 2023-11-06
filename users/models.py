from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        name,
        password,
        birth,
        phonenumber,
        nickname,
    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")
        if not password:
            raise ValueError("Users must have a password")
        if not birth:
            raise ValueError("Users must have a birth")
        if not phonenumber:
            raise ValueError("Users must have a phonenumber")
        if not nickname:
            raise ValueError("Users must have a nickname")

        user = self.model(
            email=self.normalize_email(email),
            birth=birth,
            name=name,
            password=password,
            phonenumber=phonenumber,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        birth,
        name,
        nickname,
        phonenumber,
        password,
    ):
        user = self.create_user(
            email,
            password=password,
            birth=birth,
            name=name,
            phonenumber=phonenumber,
            nickname=nickname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["birth", "name", "nickname", "phonenumber"]

    # AbstractUser에서 받아온 필드 중 수정하고 싶지 않은 필드 지정하기
    # 입력받고 싶은 필드들 작성하기
    name = models.CharField(
        max_length=30,
    )
    avatar = models.URLField(
        max_length=1000,  # 예: 1000자로 확장
        blank=True,
    )
    birth = models.CharField(
        null=True,
        max_length=10,
    )
    phonenumber = models.CharField(
        max_length=20,
    )
    nickname = models.CharField(
        max_length=30,
    )
    email = models.EmailField(
        max_length=155,
        unique=True,
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
