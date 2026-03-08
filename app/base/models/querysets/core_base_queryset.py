from django.db.models.manager import QuerySet


class CoreBaseQuerySet(QuerySet):

    # a copy of the original method of QuerySet,
    # but using CoreBaseManager instead of Manager
    def as_manager(cls):
        from base.models.managers import CoreBaseManager

        manager = CoreBaseManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)
