# Django Channels는 컨슈머(Consumer)를 통해 웹소켓 연결과 비동기 기능을 처리합니다.
# consumers.py 파일을 생성하고, 채팅 관련 컨슈머를 작성합니다:

from channels.generic.websocket import JsonWebsocketConsumer
from pprint import pprint
from typing import List
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from chats.models import RolePlayingRoom, GptMessage
import openai
<<<<<<< HEAD
from scripts.models import Script,Tag
from django.utils import timezone
from .serializers import RolePlayingRoomSerializer
=======
from scripts.models import Script, Tag
from django.utils import timezone
from .serializers import RolePlayingRoomSerializer

>>>>>>> 78771f25d52325f1587e499096393201ef388040

# 상속받은 클래스에 기본 기능 구현되어 있음
class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpt_messages: List[GptMessage] = []
        self.recommend_message: str = ""
<<<<<<< HEAD
=======
        self.room_pk = None
>>>>>>> 78771f25d52325f1587e499096393201ef388040
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
            # user가 선택한 level
            self.room_level = room.level
            # user의 초기 설정
            self.gpt_messages = room.get_initial_messages()
            # user의 level 설정
            self.room_level = room.level
            # gpt의 추천 표현
            self.recommend_message = room.get_recommend_message()
            # gpt의 초기 설정
            assistant_message = self.get_query()
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
            assistant_message = self.get_query(user_query=content_dict["message"])
            # level이 1인 경우에는 번역
            if self.room_level == 1:
                translated_message = RolePlayingRoomSerializer._translate(
                    assistant_message, "en", "ko"
                )
                assistant_message += f"({translated_message}) "
            # 아닌 경우에는 영어만
            self.send_json(
                {
                    "type": "assistant-message",
                    "message": assistant_message,
                }
            )
        elif content_dict["type"] == "request-recommend-message":
            recommended_message = self.get_query(command_query=self.recommend_message)
            self.send_json(
                {
                    "type": "recommended-message",
                    "message": recommended_message,
                }
            )
        elif content_dict["type"] == "end-save-conversation":
            # 채팅 내역 저장
            room = self.get_room()
            if room:
                message = []
                for gpt_message in self.gpt_messages:
                    message.append(gpt_message["content"])
                    # message = Script(contents=gpt_message.content)
                message = " ".join(message[2:])
                title = input("title: ")
                # Script 객체 생성 (DB에 저장)
                script = Script.objects.create(
                    title=title,
                    level=self.room_level,
                    learningDate=timezone.now(),  # 현재 날짜 사용
                    email=self.scope["user"],
                    contents=message,
                )

                # 해시태그 입력 받기
                while True:
                    hashtag_name = input("hashtag: ")
                    if hashtag_name == "":
                        break

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
        elif content_dict["type"] == "end-notsave-conversation":
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
    def get_query(self, command_query: str = None, user_query: str = None) -> str:
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
        response_content = response_dict["choices"][0]["message"]["content"]

        # 추천기능 시에는 대화내역에 추가 안함.
        if command_query is None:
            gpt_message = GptMessage(role=response_role, content=response_content)
            self.gpt_messages.append(gpt_message)

        return response_content


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
