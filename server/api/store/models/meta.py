from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.text import slugify

from core.models import BaseModel
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
