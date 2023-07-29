from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.Diaries.as_view()),
    path("<int:id>", views.DiaryDetail.as_view()),
]
