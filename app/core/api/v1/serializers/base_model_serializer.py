from typing import Any

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: Any) -> dict[str, Any]:
        data: dict[str, Any] = super().to_representation(instance)

        # if 'PYTEST_CURRENT_TEST' in os.environ:
        data["$serializer"] = self.__class__.__name__

        return data

    def get_missing_attrs(self, attrs: dict[str, Any]) -> dict[str, Any]:
        missing_attrs = (
            {
                field.name: getattr(self.instance, field.name)
                for field in self.instance._meta.fields
                if field.name not in attrs
            }
            if self.partial
            else {}
        )
        return missing_attrs

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        attrs.update(self.get_missing_attrs(attrs))
        return attrs
