from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductStoreOpts(models.Model):
    list_for_sale = models.BooleanField(
        verbose_name=_("List on store for sale"),
        default=False
    )
    sell_without_stock = models.BooleanField(
        verbose_name=_("Sell without stock"),
        help_text=_("Keep selling if product is out of stock"),
        default=False
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
        null=True
    )

    class Meta:
        verbose_name = _("Product Store Option")
        verbose_name_plural = _("Product Store Options")
        abstract = True
