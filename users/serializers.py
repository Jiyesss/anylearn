from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User

# 회원가입 기능 구현을 위한 serializer
User = get_user_model()


class UserRegistrationStep1Serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "username", "birth", "phonenumber")


class UserRegistrationStep2Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "nickname", "avatar"

    def create(self, validated_data):
        user = super().create(validated_data)

        user.email = self.context["email"]
        user.password = self.context["password"]
        user.username = self.context["username"]
        user.birth = self.context["birth"]
        user.phonenumber = self.context["phonenumber"]

        user.save()

        return user


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
