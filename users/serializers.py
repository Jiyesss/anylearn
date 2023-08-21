from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User

# 회원가입 기능 구현을 위한 serializer
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "birth", "phonenumber", "nickname", "email", "password")


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


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if user:
                attrs["user"] = user
            else:
                raise serializers.ValidationError("이메일 혹은 비밀번호가 잘못되었습니다.")
        else:
            raise serializers.ValidationError("이메일과 비밀번호를 입력해주세요.")
        return attrs
