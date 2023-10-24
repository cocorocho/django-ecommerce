from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from core.base.views import BaseGenericAPIView
from products.models import Category, Product
from products.serializers import (
    CategorySerializer,
    StoreProductSerializer,
    StoreProductDetailSerializer,
)
from products.paginators import StorePaginator


class CategoryView(RetrieveModelMixin, ListModelMixin, BaseGenericAPIView):
    lookup_field = "slug"
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.prefetch_related("sub_categories")

    def get(self, request, *args, **kwargs) -> Response:
        if kwargs.get(self.lookup_field, None):
            return self.retrieve(request, *args, **kwargs)

        response = self.list(request, *args, **kwargs)
        return response


class SubCategoryView(BaseGenericAPIView):
    """
    Retrieve View for `SubCategory` uses `Product` queryset
    for retrieving `Product(s)` of given `SubCategory` so the queryset
    can be paginated
    """

    serializer_class = StoreProductSerializer
    lookup_field = "sub_category__slug"
    pagination_class = StorePaginator

    def get_queryset(self):
        sub_category_slug = self.kwargs.get("sub_category_slug")

        return Product.objects.get_store_products().filter(
            sub_category__slug=sub_category_slug
        )

    def get(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.serializer_class(
            paginated_queryset, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class ProductView(RetrieveModelMixin, BaseGenericAPIView):
    queryset = Product.objects.get_store_products()
    serializer_class = StoreProductDetailSerializer

    def get(self, request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)
