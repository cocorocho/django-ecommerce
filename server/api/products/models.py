from django.utils.text import slugify
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from core.base.models import BaseModel, BaseManager
from products.querysets import ProductQuerySet
from products.abc.models import ProductStoreOpts


def product_image_upload_path(instance, filename) -> str:
    dir_name = f"{instance.product.manufacturer}_{instance.product.name}".replace(
        " ", "_"
    ).lower()
    return f"products/images/{dir_name}/{filename}"


class Category(BaseModel):
    """Product category"""

    name = models.CharField(
        max_length=100, verbose_name=_("Product Category"), unique=True
    )
    slug = models.SlugField(editable=False)
    banner = models.ImageField(upload_to="banners/category/", null=True)

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def save(self, *args, **kwargs) -> None:
        # Create or update slug
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class SubCategory(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_("Sub Category"), unique=True)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="sub_categories",
        verbose_name=_("Category"),
    )
    slug = models.SlugField(editable=False)
    thumbnail = models.ImageField(
        upload_to="thumbnails/sub-category/", null=True
    )  # revert null

    class Meta:
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")

    def save(self, *args, **kwargs) -> None:
        # Create or update slug
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Product(ProductStoreOpts, BaseModel):
    sku = models.CharField(max_length=100, verbose_name=_("Product SKU"), unique=True)
    manufacturer = models.CharField(max_length=100, verbose_name=_("Manufacturer"))
    name = models.CharField(max_length=100, verbose_name=_("Product Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    description_rich = RichTextField(
        blank=True, verbose_name=_("Description (WYSIWYG)")
    )
    sub_category = models.ForeignKey(
        to=SubCategory,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Sub Category"),
    )
    slug = models.SlugField(editable=False)
    stock = models.PositiveIntegerField(
        verbose_name=_("Stock"), default=0, help_text=_("Number of products in stock")
    )

    @property
    def in_stock(self) -> bool:
        return self.stock > 0

    objects = BaseManager.from_queryset(ProductQuerySet)()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return f"{self.manufacturer} - {self.name}"

    def save(self, *args, **kwargs) -> None:
        # Create or update slug
        self.slug = slugify(self.manufacturer + self.name)

        return super().save(*args, **kwargs)


class ProductImage(BaseModel):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to=product_image_upload_path,
        verbose_name=_("Image file"),
    )

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
