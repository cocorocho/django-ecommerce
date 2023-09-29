from typing import List

from rest_framework import serializers
from rest_framework.serializers import ReturnDict

from products.models import Category, SubCategory, Product
from products.serializers import ProductSerializer
from store.models import StoreProduct
from store.services.sub_category import SubCategoryService


class StoreProductsSerializer(serializers.ModelSerializer):
    """
    Includes fields with key features, no details
    """
    product = ProductSerializer()

    class Meta:
        model = StoreProduct
        fields = (
            "is_featured",
            "price",
            "product",
        )
        read_only_fields = fields


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("name", "slug", "thumbnail")


class StoreCategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("name", "sub_categories", "slug", "banner",)


class StoreCategoryWithProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("name", "slug", "products")
        read_only_fields = fields


class StoreSubCategoryProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = (
            "products",
            "name",
            "slug",
            "thumbnail"
        )
        read_only_fields = fields

    def get_products(self, obj) -> ReturnDict:
        queryset = SubCategoryService.get_store_products(obj.pk)
        return StoreProductsSerializer(queryset, many=True).data