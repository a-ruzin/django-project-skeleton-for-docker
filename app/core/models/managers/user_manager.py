from typing import Generic, TypeVar, Any, TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from base.models.managers.core_base_manager import CoreBaseManager
from core.models.querysets.user_queryset import UserQuerySet
from lib.phone import normalize_phone as normalize_phone_e164

if TYPE_CHECKING:
    from core.models import User

_UserType = TypeVar('_UserType', bound='User')


class UserManager(CoreBaseManager, models.Manager.from_queryset(UserQuerySet), BaseUserManager, Generic[_UserType]):  # type: ignore
    queryset_class = UserQuerySet

    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    @classmethod
    def normalize_phone(cls, phone: str) -> str:
        """
        Normalize the phone number to E.164 format.
        """
        normalized = normalize_phone_e164(phone)
        if normalized is None:
            raise ValueError(f"Invalid phone number: {phone}")
        return normalized

    def _create_user(self, phone: str, password: str, **extra_fields: Any) -> _UserType:
        """
        Create and save a user with the given phone, and password.
        """
        if not phone:
            raise ValueError('The given username must be set')
        phone = self.normalize_phone(phone)
        user: _UserType = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone: str, password: str | None = None, **extra_fields: Any) -> _UserType:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone: str, password: str, **extra_fields: Any) -> _UserType:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)
