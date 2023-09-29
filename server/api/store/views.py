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


class SubCategoryAPIView(RetrieveAPIView):
    """
    Retrieve endpoint for `SubCategory` using `slug` field.
    Includes `StoreProduct(s)` of `SubCategory`
    """
    queryset = SubCategoryService.get_sub_categories()
    serializer_class = StoreSubCategoryProductsSerializer
    pagination_class = StorePaginator
    lookup_field = "slug"

