__all__ = ['BaseAdmin']

from django.contrib.admin import ModelAdmin


class BaseAdmin(ModelAdmin):
    readonly_fields = ()

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request)
        if obj:
            return list(fields) + ['created_at', 'updated_at']
        else:
            return list(fields)

    def get_changelist_instance(self, request):
        cl = super().get_changelist_instance(request)
        cl.title = self.model._meta.verbose_name_plural.capitalize()
        return cl
