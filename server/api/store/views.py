from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from store.serializers import (
    StoreCategorySerializer, StoreCategoryWithProductsSerializer, CategoryProductsSerializer
)
from store.models import StoreProduct
from products.models import Category


class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.prefetch_related("sub_categories")
    serializer_class = StoreCategorySerializer


class CategoryProductsViewSet(ListAPIView):
    class Paginator(PageNumberPagination):
        page_size = 20

    serializer_class = CategoryProductsSerializer
    pagination_class = Paginator
    lookup_field = "product.sub_category.category.name"

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        category = get_object_or_404(Category, slug=category_slug)

        queryset = (
            StoreProduct.objects
                .select_related("product")
                .filter(product__sub_category__category=category)
        )

        return queryset
