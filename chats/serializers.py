from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import RolePlayingRoom
from users.models import User
from .translators import google_translate


# detail chat에서 보고 싶은 field만 보기 위한 serializer
class TinyChatSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "nickname",
            "email",
        )


# 전체 chats 보기 위한 serializer
class ChatSerializer(ModelSerializer):
    class Meta:
        model = RolePlayingRoom
        fields = "__all__"


# datil chat을 보기 위한 serializer
class ChatDetailSerializer(ModelSerializer):
    user = TinyChatSerializer()

    class Meta:
        model = RolePlayingRoom
        fields = "__all__"
        depth = 1


# 번역기능추가
class RolePlayingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePlayingRoom
        fields = [
            "id",
            "level",
            "situation",
            "situation_en",
            "my_role",
            "my_role_en",
            "gpt_role",
            "gpt_role_en",
        ]

    def validate(self, data):
        situation = data.get("situation")
        situation_en = data.get("situation_en")
        if situation and not situation_en:
            data["situation_en"] = self._translate(situation)

        my_role = data.get("my_role")
        my_role_en = data.get("my_role_en")
        if my_role and not my_role_en:
            data["my_role_en"] = self._translate(my_role)

        gpt_role = data.get("gpt_role")
        gpt_role_en = data.get("gpt_role_en")
        if gpt_role and not gpt_role_en:
            data["gpt_role_en"] = self._translate(gpt_role)

        return data

    @staticmethod
    def _translate(origin_text: str) -> str:
        translated = google_translate(origin_text, "ko", "en")
        if not translated:
            raise serializers.ValidationError("구글 번역에 실패했습니다.")
        return translated
