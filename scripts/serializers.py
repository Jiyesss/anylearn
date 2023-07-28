from rest_framework.serializers import ModelSerializer
from .models import Script


# detail화면에서 email을 간단히 보기 위한 serializer
class TinyEmailSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = ("email",)


# put요청할 때, 두가지 필드만 입력받기 위한 serializer
class ScriptTinySerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = (
            "hashtag",
            "contents",
        )


# 전체 scripts를 보기 위한 serializer
class ScriptSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = "__all__"


# datil script를 보기 위한 serializer
class ScriptDetailSerializer(ModelSerializer):
    email = TinyEmailSerializer()

    class Meta:
        model = Script
        fields = "__all__"
        depth = 1
