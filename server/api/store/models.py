from django.utils.translation import gettext_lazy as _
from django.db import models


from products.models import Product
from core.models import BaseModel


def product_image_upload_path(instance, filename) -> str:
    return f"store/product/{instance.product.product.name}/{filename}"


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
    is_listed = models.BooleanField(
        default=True,
        verbose_name=_("Listed for sale")
    )

    class Meta:
        verbose_name = _("Store Product")
        verbose_name_plural = _("Store Products")
        ordering = ["-date_created"]

    def __str__(self) -> str:
        return f"{str(self.product)} - {self.price}"


class ProductImage(BaseModel):
    product = models.ForeignKey(
        to=StoreProduct,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to=product_image_upload_path)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
