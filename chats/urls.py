from django.urls import path
from . import views

urlpatterns = [
    path("", views.Chats.as_view()),
    path("<int:pk>", views.ChatDetail.as_view()),
]
