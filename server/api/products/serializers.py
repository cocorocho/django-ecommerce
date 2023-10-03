from rest_framework import serializers

from products.models import Category, SubCategory, Product


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "manufacturer",
            "name",
            "slug"
        )
        read_only_fields = fields