from .extra_for_thing_serializer import ExtraForProductSerializer
from .thing_serializer import ThingSerializer


class ProductSerializerWithExtra(ThingSerializer):
    extra = ExtraForProductSerializer(source='*', read_only=True, required=False)

    class Meta(ThingSerializer.Meta):
        fields = ThingSerializer.Meta.fields + ['extra']
