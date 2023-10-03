from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from store.models import ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
    # def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    #     return super().get_queryset(request).select_related(
    #         "product",
    #         "product__product"
    #     )
