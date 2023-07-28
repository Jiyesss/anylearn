from django.urls import path
from . import views

urlpatterns = [
    path("", views.Diaries.as_view()),
    path("<slug:nowDate>", views.Diaries.as_view()),
]
