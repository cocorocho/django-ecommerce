from django.utils.translation import gettext_lazy as _
from django.db import models


def product_image_upload_path(instance, filename) -> str:
    return f"store/product/{instance.product.product.name}/{filename}"
