from django.utils.translation import gettext_lazy as _
from django.db import models

from core.base.models import BaseModel
from payments.models.details import AbstractAddress, Address


class Order(BaseModel):
    """
    Order details model

    Address fields will be populated from `Address` model's values.
    Address is kept as JSON field to prevent changes on address table reflecting
    on a started order
    """

    shipping_address = models.JSONField(
        verbose_name=_("shipping address"), editable=False
    )
    billing_address = models.JSONField(
        verbose_name=_("billing address"), editable=False
    )

    # TODO Order status

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
