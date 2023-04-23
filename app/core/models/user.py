__all__ = ['User']

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

from base.models import CoreModel
from .managers.user import UserManager


class User(CoreModel, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    name: str = models.CharField(_('Фамилия и имя'), max_length=256, blank=True)
    email: str = models.EmailField(_('email address'), blank=False, unique=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. ' 'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    @property
    def smart_name(self) -> str:
        return self.name or self.email

    def __str__(self) -> str:
        return self.email
