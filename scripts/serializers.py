from rest_framework.serializers import ModelSerializer
from .models import Script


class ScriptSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = (
            "title",
            "hashtag",
            "contents",
            "level",
            "learningDate",
        )


class ScriptDetailSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = "__all__"
