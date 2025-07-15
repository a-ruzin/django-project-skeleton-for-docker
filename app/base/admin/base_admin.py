from typing import Any

from django.contrib.admin import ModelAdmin
from django.db.models import Model
from django.http import HttpRequest
from modeltranslation.admin import TabbedTranslationAdmin, TranslationAdmin


class BaseAdmin(ModelAdmin):
    readonly_fields: list[str] = []

    def get_readonly_fields(self, request: HttpRequest, obj: Model = None) -> list[Any]:
        fields = super().get_readonly_fields(request)
        if obj:
            return list(fields) + ["created_at", "updated_at"]
        else:
            return list(fields)

    def get_changelist_instance(self, request: HttpRequest) -> Any:
        cl = super().get_changelist_instance(request)
        cl.title = self.model._meta.verbose_name_plural.capitalize()
        return cl


# Языковые поля имеют вкладку под каждый язык
class BaseTranslationAdmin(BaseAdmin, TabbedTranslationAdmin):
    pass


# Все языковые поля выводятся вместе
class BaseSimpleTranslationAdmin(BaseAdmin, TranslationAdmin):
    pass
