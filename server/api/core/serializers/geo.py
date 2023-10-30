from cities_light.models import Region, Country

from core.base.serializers import DynamicFieldsModelSerializer


class RegionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Region
        fields = ("name", "slug")


class CountrySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Country
        fields = ("name", "slug", "phone")
        read_only_fields = fields


class CountryDetailsSerializer(DynamicFieldsModelSerializer):
    regions = RegionSerializer(many=True, source="region_set")

    class Meta:
        model = Country
        fields = ("name", "slug", "regions")
        read_only_fields = fields
