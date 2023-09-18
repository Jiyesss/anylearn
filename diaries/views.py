from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from datetime import datetime
from .models import Diary
from .serializers import DiarySerializer, TinyDiarySerializer, DiaryDetailSerializer


# /api/v1/diaries url에 접근했을 때 API
class Diaries(APIView):
    def get(self, requet):
        all_diaries = Diary.objects.filter(user_email=self.request.user)
        serializer = DiarySerializer(
            all_diaries,
            many=True,
        )
        return Response(serializer.data)


# /api/v1/diaries/[NowDate] url에 접근했을 때 API
class DiaryDetail(APIView):
    # id가 아닌 date로 다이어리 찾아오기
    def get_object(self, date):
        try:
            convert_date = datetime.strptime(date_string, "%Y-%m-%d")
            return Diary.objects.get(nowDate=convert_date, user_email=self.request.user)
        except Diary.DoesNotExist:
            raise NotFound

    def get(self, request, date):
        diary = self.get_object(date)
        serializer = DiaryDetailSerializer(diary)
        return Response(serializer.data)

    def put(self, request, date, format=None):
        diary = self.get_object(date)
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

    def delete(self, date):
        diary = self.get_object(date)
        diary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
