from rest_framework.viewsets import ReadOnlyModelViewSet
from cities_light.models import Country

from core.serializers.geo import CountrySerializer, CountryDetailsSerializer


class CountryViewSet(ReadOnlyModelViewSet):
    queryset = Country.objects.prefetch_related("region_set")
    serializer_class = CountrySerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryDetailsSerializer

        return super().get_serializer_class()
