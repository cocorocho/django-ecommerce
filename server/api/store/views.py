from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from store.serializers import (
    StoreCategorySerializer, StoreCategoryWithProductsSerializer, StoreProductsSerializer,
    StoreSubCategoryProductsSerializer
)
from store.models import StoreProduct
from store.paginators import StorePaginator
from store.services.products import StoreProductService
from store.services.category import CategoryService
from store.services.sub_category import SubCategoryService
from products.models import Category, SubCategory


class CategoryViewSet(ReadOnlyModelViewSet):
    """
    List / Retrieve endpoint for `Category`
    Includes `SubCategory(s)` but no products
    """
    queryset = CategoryService.get_categories()
    serializer_class = StoreCategorySerializer
    lookup_field = "slug"


class SubCategoryProductsListView(ListAPIView):
    """
    Retrieve endpoint for `SubCategory` using `slug` field.
    Includes `StoreProduct(s)` of `SubCategory`
    """
    queryset = StoreProductService.get_products()
    serializer_class = StoreProductsSerializer
    pagination_class = StorePaginator

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        sub_category_slug = self.kwargs.get("sub_category_slug")
        queryset = super().get_queryset().filter(
            product__sub_category__category__slug=category_slug,
            product__sub_category__slug=sub_category_slug
        )
        return queryset
