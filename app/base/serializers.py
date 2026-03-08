from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=False)
    error_code = serializers.IntegerField()
    error_message = serializers.CharField()
    field_errors = serializers.DictField(required=False, allow_null=True)
    data = serializers.DictField(required=False, allow_null=True)
