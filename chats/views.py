from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import RolePlayingRoom
from .serializers import ChatSerializer, ChatDetailSerializer, RolePlayingRoomSerializer
from gtts import gTTS


# /api/v1/chats url에 접근했을 때 API
class Chats(APIView):
    def get(self, requet):
        all_chats = RolePlayingRoom.objects.all()
        serializer = RolePlayingRoomSerializer(
            all_chats,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RolePlayingRoomSerializer(data=request.data)
        if serializer.is_valid():
            new_chat = serializer.save(user=request.user)
            return Response(RolePlayingRoomSerializer(new_chat).data)
        else:
            return Response(serializer.errors)


class RolePlayingRoomCreateView(generics.CreateAPIView):
    queryset = RolePlayingRoom.objects.all()
    serializer_class = RolePlayingRoomSerializer


# /api/v1/chats/[pk] url에 접근했을 때 API
class ChatDetail(APIView):
    def get_object(self, pk):
        try:
            return RolePlayingRoom.objects.get(pk=pk)
        except RolePlayingRoom.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        chat = self.get_object(pk)
        serializer = ChatDetailSerializer(chat)
        return Response(serializer.data)

    def put(self, request, pk):
        chat = self.get_object(pk)
        serializer = ChatDetailSerializer(
            chat,
            data=request.data,
            partial=True,  # partial = True는 필수 항목을 수정하지 않아도 error안난다는 의미
        )
        if serializer.is_valid():
            updated_chat = serializer.save()
            return Response(
                ChatDetailSerializer(updated_chat).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        chat = self.get_object(pk)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@staff_member_required
def make_voice(request):
    lang = request.GET.get("lang", "en")
    message = request.GET.get("message")

    response = Response()
    gTTS(message, lang=lang).write_to_fp(response)
    response["Content-Type"] = "audio/mpeg"

    return response
