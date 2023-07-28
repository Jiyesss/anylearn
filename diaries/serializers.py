from rest_framework.serializers import ModelSerializer
from scripts.serializers import TinyEmailSerializer
from .models import Diary


# 전체 diareis를 보기 위한 serializer
class DiarySerializer(ModelSerializer):
    class Meta:
        model = Diary
        fields = "__all__"


# datil diary를 보기 위한 serializer
class DiaryDetailSerializer(ModelSerializer):
    user_email = TinyEmailSerializer()

    class Meta:
        model = Diary
        fields = "__all__"
        depth = 1


# put요청할 때, 두가지 필드만 입력받기 위한 serializer
class TinyDiarySerializer(ModelSerializer):
    class Meta:
        model = Diary
        fields = (
            "comments",
            "diaryContents",
        )
