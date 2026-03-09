from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

from base.models import CoreModel

from .managers import UserManager


class User(CoreModel, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"

    first_name = models.CharField(_("Имя"), max_length=256, blank=True)
    last_name = models.CharField(_("Фамилия"), max_length=256, blank=True)
    phone = models.CharField(_("Телефон"), max_length=30, unique=True)
    is_phone_confirmed = models.BooleanField(
        _("Телефон подтвержден"),
        default=False,
        help_text=_("Означает, что телефон пользователя был подтвержден."),
    )
    email = models.EmailField(_("Email"), unique=True, null=True, blank=False)
    is_email_confirmed = models.BooleanField(
        _("Email подтвержден"),
        default=False,
        help_text=_("Означает, что email пользователя был подтвержден."),
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)

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

    objects = UserManager['User']()

    class Meta:
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")

    @property
    def full_name(self) -> str:
        return ' '.join(filter(None, [self.first_name, self.last_name]))

    def __str__(self) -> str:
        return self.full_name or self.phone or self.email or f"User {self.id}"
