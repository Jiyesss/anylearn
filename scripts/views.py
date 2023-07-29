from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import Script
from .serializers import ScriptSerializer, ScriptTinySerializer, ScriptDetailSerializer


# /api/v1/scripts url에 접근했을 때 API
class Scripts(APIView):
    def get(self, requet):
        all_scripts = Script.objects.all()
        serializer = ScriptSerializer(
            all_scripts,
            many=True,
        )
        return Response(serializer.data)


# /api/v1/scripts/[pk] url에 접근했을 때 API
class ScriptDetail(APIView):
    def get_object(self, pk):
        try:
            return Script.objects.get(pk=pk)
        except Script.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        script = self.get_object(pk)
        serializer = ScriptDetailSerializer(script)
        return Response(serializer.data)

    def put(self, request, pk):
        script = self.get_object(pk)
        serializer = ScriptTinySerializer(
            script,
            data=request.data,
            partial=True,  # partial = True는 필수 항목을 수정하지 않아도 error안난다는 의미
        )
        if serializer.is_valid():
            updated_script = serializer.save()
            return Response(
                ScriptTinySerializer(updated_script).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        script = self.get_object(pk)
        script.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
