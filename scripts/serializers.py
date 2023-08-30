from django.utils import timezone
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Script, Tag
from diaries.models import Diary


# detail화면에서 email을 간단히 보기 위한 serializer
class TinyEmailSerializer(ModelSerializer):
    class Meta:
        model = Script
        fields = ("email",)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag"]


# put요청할 때, 원하는 필드만 입력받기 위한 serializer
class ScriptTinySerializer(ModelSerializer):
    hashtag = TagSerializer(many=True)

    class Meta:
        model = Script
        fields = ("hashtag", "contents", "add_diary")

    def get_serializer_context(self):
        return {"request": self.request}

    def hashtag_update(self, hashtag_data, instance):
        # 변경된 해시태그 존재 시, 업데이트 후 반환하기
        if hashtag_data is not None:
            instance.hashtag.clear()
            for tag_data in hashtag_data:
                tag, created = Tag.objects.get_or_create(tag=tag_data["tag"])
                instance.hashtag.add(tag)
        return instance

    def update(self, instance, validated_data):
        if "hashtag" in validated_data:
            # hashtag 데이터 추출 후 삭제
            hashtag_data = validated_data.pop("hashtag", [])

            # 나머지 필드 업데이트
            instance.contents = validated_data.get("contents", instance.contents)
            instance.add_diary = validated_data.get("add_diary", instance.add_diary)
            instance.save()

            # hashtag 필드 업데이트 적용
            instance = self.hashtag_update(hashtag_data, instance)

            return instance

        elif "contents" in validated_data:
            # contents 데이터 추출 및 업데이트
            instance.contents = validated_data.get("contents", instance.contents)

            # 나머지 필드 업데이트
            hashtag_data = validated_data.pop("hashtag", None)
            instance = self.hashtag_update(hashtag_data, instance)
            instance.add_diary = validated_data.get("add_diary", instance.add_diary)
            instance.save()

            return instance

        elif "add_diary" in validated_data:
            # 나머지 필드 업데이트
            instance.contents = validated_data.get("contents", instance.contents)
            hashtag_data = validated_data.pop("hashtag", None)
            instance = self.hashtag_update(hashtag_data, instance)
            instance.save()

            # add_diary == 1 이라면, Diary 객체에 새로운 object 생성하기 with instance.contents
            if validated_data.get("add_diary") == 1:
                created_diary = Diary.objects.create(
                    fromScript=instance.contents,
                    nowDate=timezone.now(),
                    comment="",
                    user_email=self.context["request"].user,
                )
                created_diary.diaryContents.add(instance)
                created_diary.save()
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
