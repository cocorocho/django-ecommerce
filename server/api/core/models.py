from django.utils.translation import gettext_lazy as _
from django.db import models


class BaseQuerySet(models.QuerySet):
    pass


class BaseManager(models.Manager):
    pass


class BaseModel(models.Model):
    """
    Abstract base model with fields:
        - `date_created`    for when instance is created
        - `date_modified`   for when instance is updated
    """
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date created")
    )
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date modified")
    )

    class Meta:
        abstract = True
