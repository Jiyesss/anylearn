"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from environ import Env
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
# .env 경로에 파일이 존재한다면, 환경변수로서 읽기
env_path: Path = BASE_DIR / ".env"
if env_path.is_file():
    with env_path.open("rt", encoding="utf-8") as f:
        env.read_env(f, overwrite=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@5q1u($b^0#-gywryihv7_8s7ewcwal+e0&a5g%8gy=%lh5n-!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 호스트의 요청을 받기 위해 호스트 등록하기
ALLOWED_HOSTS = ["*"]

# Application definition
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "scripts.apps.ScriptsConfig",
    "diaries.apps.DiariesConfig",
    "chats.apps.ChatsConfig",
]

SYSTEM_APPS = [
    "daphne",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv("GAE_APPLICATOIN", None):  # 배포했을 때는 if 절 조건을 수행
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "anylearn",
            "USER": "welearn",
            "PASSWORD": "welearn2023",
            "HOST": "/cloudsql/welearn",
        }
    }
else:  # 개발 환경일 경우에는 else 절 조건을 수행
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "anylearn_db",
            "USER": "welearn",
            "PASSWORD": "welearn2023",
            "PORT": "3306",
            "HOST": "34.64.70.4",
        }
    }
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "anylearn",  # 앞서 생성한 데이터베이스 이름으로 바꾸세요
        "USER": "root",  # Cloud SQL에서 생성한 사용자 이름으로 바꾸세요
        "PASSWORD": "welearn2023",  # Cloud SQL에서 생성한 사용자 비밀번호로 바꾸세요
        "HOST": "34.64.70.4",  # 올바른 프로젝트 아이디, 지역 및 인스턴스 이름으로 업데이트하세요
        "PORT": "3306",
    }
}
"""


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# 디폴트 안내 메세지의 언어
LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="en-us")

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth
AUTH_USER_MODEL = "users.User"

ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"

# OpenAI API Key
OPENAI_API_KEY = env.str("OPENAI_API_KEY")

# To use Django Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # 데모용 설정, 배포 환경에서는 다른 백엔드 사용을 고려
    },
}

CORS_ALLOW_WEBSOCKETS = True  # 웹소켓에 대한 CORS 허용 설정
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://192.168.88.1:8000",
    "https://hf151-395305.df.r.appspot.com",
    # 다른 허용하고자 하는 도메인을 추가할 수 있습니다.
]
