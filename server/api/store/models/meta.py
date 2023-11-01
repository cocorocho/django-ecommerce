from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.text import slugify

from core.base.models import BaseModel, SingletonModel
from store.models.abstract import StorePolicies, Socials
from store.querysets import StoreManager, StoreQuerySet
from store.exceptions import IndeletableStore
from products.models import Product


class FeaturedProducts(BaseModel):
    products = models.ManyToManyField(
        to=Product,
        related_name="featured",
    )
    image = models.ImageField(
        upload_to="store/featured/",
        verbose_name=_("Image file"),
    )
    header = models.TextField(
        verbose_name=_("Featured items header"),
        max_length=100,
    )
    slug = models.SlugField(editable=False)

    class Meta:
        verbose_name = _("featured product")
        verbose_name_plural = _("featured products")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.header)

        return super().save(*args, **kwargs)


class Store(
    Socials,
    StorePolicies,
    SingletonModel,
    BaseModel,
):
    """
    Model to store all Store related info

    This is a singleton model, can't be more than one instance
    """

    name = models.CharField(
        max_length=100, verbose_name=_("Store name"), default="My Store"
    )
    logo = models.ImageField(
        verbose_name=_("Store logo"),
        upload_to="store",
    )
    favicon = models.ImageField(
        verbose_name="Favicon",
        upload_to="store",
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=500,
        verbose_name=_("address"),
        blank=True,
    )

    objects = StoreManager.from_queryset(StoreQuerySet)()

    class Meta:
        verbose_name = _("Store Info")
        verbose_name_plural = (
            verbose_name  # Don't need plural as it is supposed to be singleton
        )

    def __str__(self) -> str:
        return self.name

    def delete(self) -> None:
        raise IndeletableStore()
