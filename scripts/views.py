from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Script
from .serializers import ScriptSerializer


# Create your views here.
class Scripts(APIView):
    def get(self, requet):
        all_scripts = Script.objects.all()
        serializer = ScriptSerializer(
            all_scripts,
            many=True,
        )
        return Response(serializer.data)
