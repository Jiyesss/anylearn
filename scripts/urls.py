from django.urls import path
from . import views

urlpatterns = [
    path("", views.Scripts.as_view()),
]
