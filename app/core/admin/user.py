from typing import Any, TypeAlias, cast

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext as _

from core.models import User

fieldsets: TypeAlias = tuple[tuple[Any | None, dict[str, tuple[str, ...]]], ...]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ("id", "email", "first_name", "last_name", "phone")

    list_display = [
        "id",
        "email",
        "created_at",
        "full_name",
        "phone",
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    list_display_links = ("email",)
    readonly_fields = ["created_at", "last_login"]
    ordering = ["-created_at"]
    list_per_page = 50
    filter_horizontal = ["groups", "user_permissions"]

    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "first_name", "last_name", "phone", "password1", "password2")},
        ),
    )

    def get_fieldsets(self, request: HttpRequest, obj: models.Model | None = None) -> fieldsets:
        if not obj:
            return cast(fieldsets, super().get_fieldsets(request, obj))

        if request.user.is_superuser:
            permissions_fields: tuple[str, ...] = (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        else:
            permissions_fields = ("is_active",)

        return (
            (None, {"fields": ("email", "password")}),
            (_("Персональная информация"), {"fields": ("first_name", "last_name", "phone", "language")}),
            (_("Разрешения"), {"fields": permissions_fields}),
            (_("Даты"), {"fields": ("last_login", "created_at")}),
        )
