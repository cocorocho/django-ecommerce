from django.db.models import QuerySet, Prefetch

from products.models import Category, SubCategory


class CategoryService:
    @staticmethod
    def get_categories() -> QuerySet[Category]:
        """
        Get `Category` queryset which have any `StoreProduct(s)`
        """
        return Category.objects.prefetch_related(
            Prefetch(
                "sub_categories",
                SubCategory.objects.all()
            )
        )