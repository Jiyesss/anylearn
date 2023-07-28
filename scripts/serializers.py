from rest_framework.serializers import ModelSerializer
from .models import Script


class TinyEmailSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = ("email",)


class ScriptTinySerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = (
            "hashtag",
            "contents",
        )


class ScriptSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = "__all__"


class ScriptDetailSerializer(ModelSerializer):
    email = TinyEmailSerializer()

    class Meta:
        model = Script
        fields = "__all__"
        depth = 1
