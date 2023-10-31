from django.db.models import QuerySet

from products.models import Product
from store.models import FeaturedProducts
from products.querysets import ProductQuerySet


class StoreProductService:
    @staticmethod
    def get_products() -> ProductQuerySet:
        """
        Get `StoreProduct(s)` which are to be listed on store.
        `is_listed` field is used for filtering the queryset.
        """
        return (
            Product.objects.filter(list_for_sale=True)
            .select_related("product")
            .prefetch_related("images")
        )

    @staticmethod
    def get_sub_category_products(sub_category_slug: str) -> ProductQuerySet:
        return Product.objects.all()

    @staticmethod
    def get_featured() -> ProductQuerySet:
        """
        Get featured products

        :param bool details: Include product details
        """
        # Add products with details / Array agg, no serializer required
        return FeaturedProducts.objects.prefetch_related("products", "products__images")
