from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import Diary
from .serializers import DiarySerializer, TinyDiarySerializer, DiaryDetailSerializer


# /api/v1/diaries url에 접근했을 때 API
class Diaries(APIView):
    def get(self, requet):
        all_diaries = Diary.objects.all()
        serializer = DiarySerializer(
            all_diaries,
            many=True,
        )
        return Response(serializer.data)


# /api/v1/diaries/[pk] url에 접근했을 때 API
class DiaryDetail(APIView):
    def get_object(self, pk):
        try:
            return Diary.objects.get(pk=pk)
        except Diary.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        diary = self.get_object(pk)
        serializer = DiaryDetailSerializer(diary)
        return Response(serializer.data)

    def put(self, request, pk):
        diary = self.get_object(pk)
        serializer = TinyDiarySerializer(
            diary,
            data=request.data,
            partial=True,  # partial = True는 필수 항목을 수정하지 않아도 error안난다는 의미
        )
        if serializer.is_valid():
            updated_diary = serializer.save()
            return Response(
                TinyDiarySerializer(updated_diary).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        diary = self.get_object(pk)
        diary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
