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
        fields = ("id","tag",)


# put요청할 때, 두가지 필드만 입력받기 위한 serializer
class ScriptTinySerializer(ModelSerializer):
    hashtag = TagSerializer(many=True)

    class Meta:
        model = Script
        fields = ("hashtag", "contents")

    def update(self, instance, validated_data):
        hashtag_data = validated_data.pop('hashtag', [])
        
        # Update the associated tags for the script
        for tag_data in hashtag_data:
            tag_id = tag_data.get('id', None)
            tag_tag = tag_data.get('tag', None)

            if tag_id and tag_tag:
                try:
                    tag = Tag.objects.get(pk=tag_id)
                    tag.tag = tag_tag
                    tag.save()
                except Tag.DoesNotExist:
                    # If the tag with the given ID doesn't exist, you can handle it here
                    pass
        instance.contents = validated_data.get('contents', instance.contents)
        # Update other fields as needed...

        instance.save()
        return instance          


# 전체 scripts를 보기 위한 serializer
class ScriptSerializer(ModelSerializer):
    hashtag = SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='tag',
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

