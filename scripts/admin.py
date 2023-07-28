from django.contrib import admin
from .models import Script


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "hashtag_list",
        "contents",
        "level",
        "learningDate",
    ]

    def hashtag_list(self):
        return Script.hashtag


@admin.register
class TagAdmin(admin.ModelAdmin):
    pass
