from django.utils.text import slugify
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_jsonform.models.fields import JSONField

from core.models import BaseModel


class Category(BaseModel):
    """Product category"""

    name = models.CharField(
        max_length=100,
        verbose_name=_("Product Category"),
        unique=True
    )
    slug = models.SlugField(editable=False)

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def save(self, *args, **kwargs) -> None:
        # Generate slug on create
        if not self.pk:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    

class SubCategory(BaseModel):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Sub Category"),
        unique=True
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="sub_categories",
        verbose_name=_("Category")
    )
    slug = models.SlugField(editable=False)

    class Meta:
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")

    def save(self, *args, **kwargs) -> None:
        # Generate slug on create
        if not self.pk:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    ATTRIBUTES_SCHEMA = {
        "type": "dict",
        "keys": {
            "_reserved": {
                "type": "string",
                "widget": "hidden",
                "readonly": True
            }
        },
        "additionalProperties": True
    }

    sku = models.CharField(
        max_length=100,
        verbose_name=_("Product SKU"),
        unique=True
    )
    manufacturer = models.CharField(
        max_length=100,
        verbose_name=_("Manufacturer")
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("Product Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    attributes = JSONField(
        verbose_name=_("Product attributes"),
        schema=ATTRIBUTES_SCHEMA
    )
    sub_category = models.ForeignKey(
        to=SubCategory,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Sub Category")
    )
    slug = models.SlugField(editable=False)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return f"{self.manufacturer} - {self.name}"

    def save(self, *args, **kwargs) -> None:
        # Generate slug on create
        if not self.pk:
            self.slug = slugify(self.manufacturer + self.name)

        return super().save(*args, **kwargs)
