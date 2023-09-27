from django.utils.translation import gettext_lazy as _
from django.db import models


from products.models import Product
from core.models import BaseModel


class StoreProduct(BaseModel):
    product = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name=_("Store Product")
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Featured"),
        help_text=_("Whether this product should be showed as featured product")
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _("Store Product")
        verbose_name_plural = _("Store Products")
        ordering = ["-date_created"]
