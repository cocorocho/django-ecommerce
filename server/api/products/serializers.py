from rest_framework import serializers

from core.base.serializers import DynamicFieldsModelSerializer
from products.models import Category, SubCategory, Product, ProductImage
from store.utils import create_seo_description


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("name", "slug", "thumbnail")


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("name", "slug", "banner", "sub_categories")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)
        read_only_fields = fields


class StoreProductSerializer(DynamicFieldsModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "sku",
            "manufacturer",
            "name",
            "price",
            "slug",
            "images",
            "thumbnail",
            "in_stock",
        )


class StoreProductDetailSerializer(StoreProductSerializer):
    description_short = serializers.SerializerMethodField()

    class Meta(StoreProductSerializer.Meta):
        fields = (
            "id",
            "sku",
            "manufacturer",
            "name",
            "price",
            "slug",
            "images",
            "description",
            "description_short",
            "description_rich",
            "in_stock",
            "thumbnail",
        )

    def get_description_short(self, obj: Product) -> str:
        return create_seo_description(obj.description)
