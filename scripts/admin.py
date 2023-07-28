from django.contrib import admin
from .models import Script, Tag


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "contents",
        "level",
        "learningDate",
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
