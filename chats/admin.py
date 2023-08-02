from django.contrib import admin
from .models import RolePlayingRoom


@admin.register(RolePlayingRoom)
class ChatAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "level",
        "situation",
        "my_role",
        "gpt_role",
    ]
