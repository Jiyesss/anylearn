from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomerUserAdmin(UserAdmin):
    # admin/Users에서 user를 선택했을 때 뜨는 화면
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "name",
                    "password",
                    "avatar",
                    "birth",
                    "phonenumber",
                    "nickname",
                    "email",
                )
            },
        ),
    )
    # admin/Users에서 보이는 화면
    list_display = [
        "username",
        "password",
        "avatar",
        "birth",
        "phonenumber",
        "nickname",
        "email",
    ]
