from django.urls import path, register_converter
from . import views
from django.urls.converters import StringConverter


class DateConverter(StringConverter):
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(DateConverter, "date")

urlpatterns = [
    path("", views.Diaries.as_view()),
    path("<date:date>", views.DiaryDetail.as_view()),
]
