from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from cities_light.models import Country, Region

from core.models import BaseModel


class AbstractAddress(models.Model):
    """
    Abstract Address model with address related fields
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_("address name"),
        help_text=_("Ex: home, work"),
        blank=True,
    )
    country = models.ForeignKey(
        to=Country,
        on_delete=models.PROTECT,
        related_name="country_addresses",
        verbose_name=_("Country"),
    )
    city = models.ForeignKey(
        to=Region,
        on_delete=models.PROTECT,
        related_name=("city_addresses"),
        verbose_name=_("City"),
    )
    postal_code = models.CharField(
        max_length=6,
        validators=[RegexValidator("^[0-9]{6}$", _("Invalid postal code"))],
        verbose_name=_("postal code"),
    )
    address = models.CharField(max_length=500, verbose_name=_("address"))
    phone = models.CharField(max_length=12, blank=True, verbose_name=_("phone"))

    class Meta:
        abstract = True


class Address(AbstractAddress, BaseModel):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("user"),
        related_name=_("addresses"),
    )

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
