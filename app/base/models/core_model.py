# TODO: uncomment or remove the id field if you want to use UUID as primary key instead of the default auto-incrementing integer.
# import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .core_base_model import CoreBaseModel
from .utils import model_repr


class CoreModel(CoreBaseModel):
    class Meta:
        abstract = True

    # TODO: uncomment or remove the id field if you want to use UUID as primary key instead of the default auto-incrementing integer.
    # id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False
    # )
    created_at = models.DateTimeField(_("дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("дата последнего изменения"), auto_now=True)

    __repr__ = model_repr("id")
