from django.contrib import admin
from .models import Script


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "title",
                    "hashtag_list",
                    "contents",
                    "level",
                    "learningDate",
                )
            },
        ),
    )

    list_display = [
        "title",
        "hashtag_list",
        "contents",
        "level",
        "learningDate",
    ]

    def hashtag_list(self):
        return Script.hashtag
