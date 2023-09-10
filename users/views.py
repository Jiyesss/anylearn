from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from users.models import User
from . import serializers
from .serializers import (
    UserRegistrationStep1Serializer,
    UserRegistrationStep2Serializer,
)


class Me(APIView):
    permission_classes = [IsAuthenticated]  # /me가
    # 로그인한 user의 정보를 보여줘야하는데 private해야 함

    # 나에 대한 정보를 볼 수 있다!!
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        # PrivateUserSerializer도 방금 만들었음
        return Response(serializer.data)

    # 근데 is_superuser같은 부분은 수정하면 안 되니까
    # serializer에서 제외시켜주기
    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        # step1) user가 보낸 data에서 password를 가져옴
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data)
        # password에 대한 검증만 해주면 돼
        if serializer.is_valid():
            # step2) user를 db에 저장
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


# 인증되지 않은 사용자가 url을 호출하지 못하도록 막을 것임
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            raise ParseError
        user = authenticate(
            request,
            email=email,
            password=password,
        )
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                    "session_id": request.session.session_key,
                    "user_id": user.pk,
                    "email": user.email,
                    "ok": "Welcome!",
                }
            )
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationStep1Serializer

    def create(self, request, *args, **kwargs):
        # URL 경로나 쿼리 파라미터 등에서 세션 키를 가져온다.
        session_key = kwargs.get("session_key")

        try:
            session_data = Session.objects.get(session_key=session_key).get_decoded()
        except Session.DoesNotExist:
            return Response(
                {"error": "Invalid session key."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 첫 번째 단계 시리얼라이저를 사용하여 데이터 검증
        serializer_step1 = self.get_serializer(
            data=session_data, context={"request": request}
        )

        # 두 번째 단계로 넘어가기 전에 세션 데이터에서 필요한 데이터를 추출
        if serializer_step1.is_valid():
            email = session_data.get("email")
            password_hashed = session_data.get("password")
            username = session_data.get("username")
            birth = session_data.get("birth")
            phonenumber = session_data.get("phonenumber")

            # 첫 번째 단계 데이터를 저장
            user = serializer_step1.save()

            if (
                not email
                or not password_hashed
                or not username
                or not birth
                or not phonenumber
            ):
                return Response(
                    {"error": "Incomplete registration data."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 두 번째 단계로 넘어가기 위해 두 번째 시리얼라이저로 변경
            self.serializer_class = UserRegistrationStep2Serializer

            serializer_context = {
                "request": request,
                "email": email,
                "password": password_hashed,
                "username": username,
                "birth": birth,
                "phonenumber": phonenumber,
            }

            serializer_step2 = self.get_serializer(
                data=request.data, context=serializer_context
            )
            if serializer_step2.is_valid():
                # password을 해시화 한 후 저장
                user = serializer_step2.save(
                    password=make_password(serializer_step2.validated_data["password"])
                )
                return Response(
                    {"message": "회원가입이 성공적으로 완료되었습니다."}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer_step2.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer_step1.errors, status=status.HTTP_400_BAD_REQUEST)
