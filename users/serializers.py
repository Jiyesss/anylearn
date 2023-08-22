<<<<<<< HEAD
from rest_framework.serializers import ModelSerializer
=======
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
>>>>>>> ef71a62 (토큰 인증 로그인 방법)
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )

class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
		# 수정하면 안 될 부분 
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_active",
            "name",
            "groups",
            "user_permissions",
<<<<<<< HEAD
        )
=======
        )
