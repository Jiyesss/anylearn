from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Script, Tag


# detail화면에서 email을 간단히 보기 위한 serializer
class TinyEmailSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = ("email",)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag"]


# put요청할 때, 두가지 필드만 입력받기 위한 serializer
class ScriptTinySerializer(ModelSerializer):
    hashtag = TagSerializer(many=True)

    class Meta:
        model = Script
        fields = ("hashtag", "contents")

    def update(self, instance, validated_data):
        # hashtag 데이터 추출 후 삭제
        hashtag_data = validated_data.pop("hashtag", [])

        # Update other fields as needed...
        instance.contents = validated_data.get("contents", instance.contents)
        instance.save()

        # Update the associated tags for the script
        instance.hashtag.clear()
        for tag_data in hashtag_data:
            tag, created = Tag.objects.get_or_create(tag=tag_data["tag"])
            instance.hashtag.add(tag)

        return instance


# 전체 scripts를 보기 위한 serializer
class ScriptSerializer(ModelSerializer):
    hashtag = SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field="tag",
        many=True,
    )

    class Meta:
        model = Script
        fields = "__all__"


# datil script를 보기 위한 serializer
class ScriptDetailSerializer(ModelSerializer):
    email = TinyEmailSerializer()
    hashtag = TagSerializer(many=True)

    class Meta:
        model = Script
        fields = "__all__"
