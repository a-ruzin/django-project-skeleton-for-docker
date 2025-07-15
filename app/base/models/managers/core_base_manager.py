__all__ = ("CoreBaseManager",)

from django.db.models import Manager

from ..querysets.core_base_queryset import CoreBaseQuerySet


class CoreBaseManager(Manager.from_queryset(CoreBaseQuerySet)):  # type: ignore
    pass
