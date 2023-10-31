# Django Channels는 컨슈머(Consumer)를 통해 웹소켓 연결과 비동기 기능을 처리합니다.
# consumers.py 파일을 생성하고, 채팅 관련 컨슈머를 작성합니다:

from channels.generic.websocket import JsonWebsocketConsumer
from pprint import pprint
from typing import List
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from chats.models import RolePlayingRoom, GptMessage
import openai
from scripts.models import Script, Tag
from django.utils import timezone
from .serializers import RolePlayingRoomSerializer


# 상속받은 클래스에 기본 기능 구현되어 있음
class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpt_messages: List[GptMessage] = []
        self.recommend_message: str = ""
        self.room_pk = None
        self.room_level = 1

    # 웹소켓 접속 유저가 원하는 채팅방과 연결(connect)
    def connect(self):
        room = self.get_room()
        if room is None:
            self.close()
        else:
            self.accept()

            # room_pk값
            room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
            # user의 초기 설정
            self.gpt_messages = room.get_initial_messages()
            # user의 level 설정
            self.room_level = room.level
            # gpt의 추천 표현
            self.recommend_message = room.get_recommend_message()
            # gpt의 초기 설정
            assistant_message = self.get_query()
            # gpt의 초기 설정 후 레벨 별 자막 반환
            if self.room_level in [1, 2, 3]:
                translated_message = RolePlayingRoomSerializer._translate(
                    assistant_message, "en", "ko"
                )
                assistant_message += f"({translated_message})"
            # client로 전송
            self.send_json(
                {
                    "type": "assistant-message",
                    "message": assistant_message,
                }
            )

    # client->server: receive_json
    # server->client: send_json
    def receive_json(self, content_dict, **kwargs):
        # user의 메세지를 받아서
        if content_dict["type"] == "user-message":
            assistant_message, translated_message = self.get_query(
                user_query=content_dict["message"]
            )
            """
            # level 모두 한글 자막 보내기
            if self.room_level in [1, 2, 3]:
                translated_message = RolePlayingRoomSerializer._translate(
                    assistant_message, "en", "ko"
                )
                assistant_message += f"({translated_message}) "
            """
            # 아닌 경우에는 영어만
            self.send_json(
                {
                    "type": "assistant-message",
                    "message": f"{assistant_message}({translated_message})",
                }
            )
        elif content_dict["type"] == "request-recommend-message":
            recommended_message, translated_message = self.get_query(
                command_query=self.recommend_message
            )
            self.send_json(
                {
                    "type": "recommended-message",
                    "message": f"{recommended_message}({translated_message})",                }
            )

        # 종료하기
        elif content_dict["type"] == "end-conversation":
            self.send_json(
                {
                    "type": "assistant-message",
                    "message": "",  # 종료 후, tts 기능을 위해 공백 전달
                }
            )

        # 저장함
        elif content_dict["type"] == "save":
            # 채팅 내역 저장
            room = self.get_room()
            if room:
                message = []
                for gpt_message in self.gpt_messages:
                    message.append(gpt_message["content"] + "\n")
                    # message = Script(contents=gpt_message.content)
                message = " ".join(message[2:])

                # Script 객체 생성 (DB에 저장)
                script = Script.objects.create(
                    title=content_dict["title"],  # 수정된 부분
                    level=self.room_level,
                    learningDate=timezone.now(),  # 현재 날짜 사용
                    email=self.scope["user"],
                    contents=message,
                    add_diary=0,
                )

                # 해시태그 입력 받기
                for hashtag_name in content_dict["hashtags"]:  # 수정된 부분
                    # 해시태그 DB에 저장 (이미 존재한다면 가져오기)
                    hashtag, created = Tag.objects.get_or_create(tag=hashtag_name)

                    # Script와 연결
                    script.hashtag.add(hashtag)  # add() 함수 사용

                script.save()  # 변경 사항 DB에 저장

            # 변수 초기화
            self.gpt_messages.clear()
            self.recommend_message = ""

            # 웹소켓 연결 종료
            self.close()

        # 저장안함.
        elif content_dict["type"] == "notSave":
            # 채팅 내역 저장 안함
            room = self.get_room()
            # 변수 초기화
            self.gpt_messages.clear()
            self.recommend_message = ""
            # 웹소켓 연결 종료
            self.close()

        else:
            self.send_json(
                {
                    "type": "error",
                    "message": f"Invalid type: {content_dict['type']}",
                }
            )

    # user의 채팅방 조회
    def get_room(self, **kwargs) -> RolePlayingRoom | None:
        user: AbstractUser = self.scope["user"]
        room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        room: RolePlayingRoom = None

        if user.is_authenticated:
            try:
                room = RolePlayingRoom.objects.get(pk=room_pk, user=user)
            except RolePlayingRoom.DoesNotExist:
                pass

        return room

    # openai api함수를 호출하는 메소드
    def get_query(
        self, command_query: str = None, user_query: str = None
    ) -> tuple[str, str]:
        if command_query is not None and user_query is not None:
            raise ValueError("command_query 인자와 user_query 인자는 동시에 사용할 수 없습니다.")
        elif command_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=command_query))
        elif user_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=user_query))

        response_dict = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.gpt_messages,
            temperature=1,
        )
        response_role = response_dict["choices"][0]["message"]["role"]
        response_content = response_dict["choices"][0]["message"][
            "content"
        ]  # 단일 문자열 반환됨

        print(response_content, type(response_content))

        # 번역된 문장을 script에 추가하기 위해.
        translated_message = RolePlayingRoomSerializer._translate(
            response_content, "en", "ko"  # 번역하고자 하는 문장을 인자로 전달
        )

        # 추천기능 시에는 대화내역에 추가 안함.
        if command_query is None:
            gpt_message = GptMessage(
                role=response_role, content=f"{response_content}({translated_message})"
            )
            self.gpt_messages.append(gpt_message)

        return response_content, translated_message


class MyConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_json(
            {
                "type": "connect-message",
                "message": "connect successd",
            }
        )

    def disconnect(self, close_code):
        pass

    def receive_json(self, text_data):
        message = text_data["message"]
        self.send_json(
            {
                "type": "text",
                "message": message,
            }
        )
