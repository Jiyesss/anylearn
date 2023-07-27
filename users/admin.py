from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomerUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "name",
                    "avatar",
                    "birth",
                    "phonenumber",
                    "nickname",
                    "email",
                )
            },
        ),
    )

    list_display = [
        "username",
        "avatar",
        "birth",
        "phonenumber",
        "nickname",
        "email",
    ]
