from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.api.v1.serializers.base_model_serializer import BaseModelSerializer
from core.models import UserRegistrationRequest, User
from lib.phone import normalize_phone


class UserRegistrationRequestSerializerForCreate(BaseModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = UserRegistrationRequest
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True, 'allow_null': True},
            'phone': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': _("Пароли не совпадают")})

        raw_phone = (data.get('phone') or '').strip()
        phone = normalize_phone(raw_phone) if raw_phone else None
        email = data.get('email', '').strip()

        if raw_phone and not phone:
            raise serializers.ValidationError({'phone': _("Некорректный номер телефона")})

        if not phone:
            raise serializers.ValidationError({'phone': _("Должен быть указан телефон")})

        # нормализуем в validated_data (важно для create() и проверок уникальности)
        data['phone'] = phone
        data['email'] = email or None

        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({
                'phone': _("Этот номер уже зарегистрирован. Войдите в аккаунт или воспользуйтесь восстановлением пароля.")
            })

        # Проверка дубликата UserRegistrationRequest по phone — во view,
        # т.к. там нужна особая логика (переиспользование заявки с новым кодом).

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': _("Пользователь с таким email уже существует")})

        if email and UserRegistrationRequest.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': _("Запрос на регистрацию с таким email уже существует")})

        return data

    def create(self, validated_data):
        validated_data['expires_at'] = timezone.now() + timedelta(hours=24)

        request = self.context.get('request')
        if request:
            validated_data['ip_address'] = request.META.get('REMOTE_ADDR')
            validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')

        return super().create(validated_data)
