from rest_framework import serializers


class ConfirmationByCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
