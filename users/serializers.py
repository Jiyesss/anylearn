from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
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
        )
