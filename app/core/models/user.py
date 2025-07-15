from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

from base.models import CoreModel

from .managers import UserManager


class User(CoreModel, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"

    first_name: str = models.CharField(_("Имя"), max_length=256, blank=True)
    last_name: str = models.CharField(_("Фамилия"), max_length=256, blank=True)
    phone: str = models.CharField(_("Телефон"), max_length=30, blank=True)
    email: str = models.EmailField(_("Email"), blank=False, unique=True)
    language: str = models.CharField(_("Язык"), max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_RU)

    is_staff = models.BooleanField(
        _("Штатный сотрудник"),
        default=False,
        help_text=_("Означает, что пользователь может заходить в панель администрирования."),
    )
    is_active = models.BooleanField(
        _("Активный"),
        default=True,
        help_text=_(
            "Означает, что пользователь может авторизоваться на сайте. "
            "Снимите галочку, чтобы пользователь не мог им пользоваться."
        ),
    )

    # https://id.kokocgroup.ru - fields:
    workspace = models.ForeignKey(
        'core.Workspace', on_delete=models.PROTECT, related_name='users', blank=True, null=True
    )
    kid_id: str = models.CharField(_("KID ID"), max_length=64, blank=True, null=True, unique=True)
    # end of https://id.kokocgroup.ru - fields

    objects = UserManager()

    class Meta:
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'

    def __str__(self) -> str:
        return self.email
