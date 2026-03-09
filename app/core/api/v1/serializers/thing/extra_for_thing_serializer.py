from rest_framework import serializers

from core.api.v1.serializers.workspace import WorkspaceSerializer


class ExtraForProductSerializer(serializers.Serializer):
    workspace = WorkspaceSerializer()
