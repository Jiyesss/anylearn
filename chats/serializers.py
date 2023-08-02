from rest_framework.serializers import ModelSerializer
from .models import RolePlayingRoom
from users.models import User


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
