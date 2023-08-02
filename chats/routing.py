# 라우팅 설정을 통해 컨슈머와 URL을 연결합니다.

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:room_pk>/", consumers.RolePlayingRoomConsumer.as_asgi()),
]
