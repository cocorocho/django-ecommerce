from rest_framework import serializers

from products.models import Category, SubCategory, Product
from products.serializers import ProductSerializer
from store.models import StoreProduct


class CategoryProductsSerializer(serializers.ModelSerializer):
    """
    Includes fields with key features, no details
    """
    product = ProductSerializer()

    class Meta:
        model = StoreProduct
        fields = (
            "is_featured",
            "price",
            "product"
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
        fields = ("name", "sub_categories", "slug")


class StoreCategoryWithProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("name", "slug", "products")
        read_only_fields = fields
