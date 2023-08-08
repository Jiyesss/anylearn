# 라우팅 설정을 통해 컨슈머와 URL을 연결합니다.

from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chats/(?P<room_pk>\d+)/$", consumers.RolePlayingRoomConsumer.as_asgi()
    ),
]
