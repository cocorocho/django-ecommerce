import uuid
from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

from payments.constants import CHECKOUT_EXPIRE_AGE
from core.models import BaseModel, BaseManager
from store.models.cart import Cart
from payments.querysets import CheckoutQuerySet


class AbstractPriceData(models.Model):
    """
    Abstract Model for Checkout data
    """

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("price"),
        editable=False,
        help_text="To be populated by cart's total price at creation time",
    )

    class Meta:
        abstract = True


class Checkout(AbstractPriceData, BaseModel):
    token = models.UUIDField(
        verbose_name=_("token"), editable=False, default=uuid.uuid4
    )
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.PROTECT,
        verbose_name=_("cart"),
        related_name="checkouts",
    )
    checkout_complete = models.BooleanField(
        default=False,
        verbose_name=_("Checkout complete"),
    )
    order = models.OneToOneField(
        to="payments.Order",
        on_delete=models.PROTECT,
        null=True,  # Initially Null, will be populated on finalization
        blank=True,
        verbose_name=_("order"),
    )

    objects = BaseManager.from_queryset(CheckoutQuerySet)()

    class Meta:
        verbose_name = "Checkout"
        verbose_name_plural = "Checkouts"

    def finalize_checkout(self) -> None:
        """
        Set `checkout_complete` as `True`
        """
        self.checkout_complete = True
        self.save()

    @property
    def is_expired(self) -> bool:
        """
        Determine if `checkout` session is expired
        """
        expire_date = self.date_created + timedelta(seconds=CHECKOUT_EXPIRE_AGE)
        return timezone.now() >= expire_date
