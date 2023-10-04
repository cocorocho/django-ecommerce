from django.db.models import QuerySet

from core.models import BaseQuerySet


class ProductQuerySet(BaseQuerySet):
    def get_store_products(self) -> QuerySet:
        return self.filter(
            list_for_sale=True
        ).prefetch_related(
            "images"
        ).order_by(
            "manufacturer"
        )
