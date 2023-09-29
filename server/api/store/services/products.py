from django.db.models import QuerySet

from store.models import StoreProduct


class StoreProductService:
    @staticmethod
    def get_products() -> QuerySet[StoreProduct]:
        """
        Get `StoreProduct(s)` which are to be listed on store.
        `is_listed` field is used for filtering the queryset.
        """
        return StoreProduct.objects.filter(
            is_listed=True
        ).select_related(
            "product"
        ).prefetch_related(
            "images"
        )
    
    @staticmethod
    def get_sub_category_products(sub_category_slug: str) -> QuerySet[StoreProduct]:
        return StoreProduct.objects.all()
