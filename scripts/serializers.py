from rest_framework.serializers import ModelSerializer
from .models import Script


class TinyEmailSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = ("email",)


class ScriptSerializer(ModelSerializer):
    email = TinyEmailSerializer()

    class Meta:
        model = Script
        fields = "__all__"
        depth = 1


class ScriptDetailSerializer(ModelSerializer):
    email = TinyEmailSerializer()

    class Meta:
        model = Script
        fields = "__all__"
        depth = 1
