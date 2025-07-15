from django.db import models

from .managers import CoreBaseManager
from .utils import model_repr


class CoreBaseModel(models.Model):
    class Meta:
        abstract = True

    objects = CoreBaseManager()

    __repr__ = model_repr()
