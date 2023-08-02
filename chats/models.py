from django.db import models
from django.conf import settings
from django.urls import reverse
from typing import List, TypedDict, Literal


class GptMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class RolePlayingRoom(models.Model):
    # 선택지 생성 class
    class Level(models.IntegerChoices):
        BEGINNER = 1, "초급"
        INTERMEDIATE = 2, "중급"
        ADVANCED = 3, "고급"

    # 이 모델(RolePlayingRoom)로 부터 파생되는 QuerySet의 default 정렬방향 지정
    class Meta:
        ordering = ["-pk"]

    # user 필드를 외래키로 지정
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chats",
    )
    # level 필드(1,2,3)-> 선택지
    level = models.SmallIntegerField(
        choices=Level.choices, default=Level.BEGINNER, verbose_name="레벨"
    )
    # situation 필드 -> 한글 저장
    # situation_en 필드 -> 영문 저장
    situation = models.CharField(max_length=100, verbose_name="상황")
    situation_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="상황 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, situation 필드를 번역하여 자동 반영됩니다.",
    )
    my_role = models.CharField(max_length=100, verbose_name="내 역할")
    my_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="내 역할 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, my_role 필드를 번역하여 자동 반영됩니다.",
    )
    gpt_role = models.CharField(max_length=100, verbose_name="GPT 역할")
    gpt_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="GPT 역할 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, gpt_role 필드를 번역하여 자동 반영됩니다.",
    )

    def get_absolute_url(self) -> str:
        return reverse("role_playing_room_detail", args=[self.pk])

    def get_initial_messages(self) -> List[GptMessage]:
        gpt_name = "RolePlayingBot"
        situation_en = self.situation_en
        my_role_en = self.my_role_en
        gpt_role_en = self.gpt_role_en

        if self.level == self.Level.BEGINNER:
            level_string = f"a beginner in English"
            level_word = "simple"
        elif self.level == self.Level.INTERMEDIATE:
            level_string = f"a intermediate in English"
            level_word = "intermediate"
        elif self.level == self.Level.ADVANCED:
            level_string = f"a advanced learner in English"
            level_word = "advanced"
        else:
            raise ValueError(f"Invalid level : {self.level}")

        system_message = (
            f"You are helpful assistant supporting people learning English. "
            f"Your name is {gpt_name}. "
            f"Please assume that the user you are assisting is {level_string}. "
            f"And please write only the sentence without the character role."
        )

        user_message = (
            f"Let's have a conversation in English. "
            f"Please answer in English only "
            f"without providing a translation. "
            f"And please don't write down the pronunciation either. "
            f"Let us assume that the situation in '{situation_en}'. "
            f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
            f"Please make sure that I'm {level_string}, so please use {level_word} words "
            f"as much as possible. Now, start a conversation with the first sentence!"
        )

        return [
            GptMessage(role="system", content=system_message),
            GptMessage(role="user", content=user_message),
        ]

    # 추천 표현 받기
    def get_recommend_message(self) -> str:
        level = self.level

        if level == self.Level.BEGINNER:
            level_word = "simple"
        elif level == self.Level.INTERMEDIATE:
            level_word = "intermediate"
        elif level == self.Level.ADVANCED:
            level_word = "advanced"
        else:
            raise ValueError(f"Invalid level : {level}")

        return (
            f"Can you please provide me an {level_word} example "
            f"of how to respond to the last sentence "
            f"in this situation, without providing a translation "
            f"and any introductory phrases or sentences."
        )
