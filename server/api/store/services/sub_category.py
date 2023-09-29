from django.db.models import QuerySet, Prefetch

from products.models import SubCategory, Product
from store.models import StoreProduct
from store.services.products import StoreProductService

class SubCategoryService:
    @staticmethod
    def get_sub_categories() -> QuerySet[SubCategory]:
        return SubCategory.objects.prefetch_related(
            Prefetch(
                "products",
                Product.objects.filter(storeproduct__is_listed=True).select_related(
                    "storeproduct"
                )
            )
        )

    @staticmethod
    def get_store_products(sub_category_pk: int) -> QuerySet[StoreProduct]:
        """
        Get `StoreProduct(s)` of a `SubCategory`.
        `StoreProductService` is used for getting `StoreProduct(s)` queryset, including
        joins.

        :param int sub_category_pk: PK of `SubCategory` instance
        """
        return (
            StoreProductService
                .get_products()
                .filter(product__sub_category__pk=sub_category_pk)
        )
    