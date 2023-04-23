__all__ = ['UserManager']

from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from base.models.managers.core_base_manager import CoreBaseManager
from core.models.querysets.user import UserQuerySet


class UserManager(CoreBaseManager, models.Manager.from_queryset(UserQuerySet), BaseUserManager):  # type: ignore
    queryset_class = UserQuerySet

    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def _create_user(self, email: str, password: str, **extra_fields: Any) -> models.Model:
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> models.Model:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> models.Model:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
