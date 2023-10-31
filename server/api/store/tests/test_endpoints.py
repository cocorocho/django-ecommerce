from model_bakery import baker
from rest_framework.reverse import reverse

from core.test import BaseTestCase
from store.services.products import StoreProductService
from store.serializers import FeaturedProductsReadOnlySerializer


class StoreProductsTestCase(BaseTestCase):
    def test_list_featured_products(self) -> None:
        products = baker.make(
            "store.FeaturedProducts", header="test", _quantity=5, make_m2m=True
        )

        url = reverse("store:featured-product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_response = list(
            StoreProductService.get_featured().values("id", "image", "header", "slug")
        )
        self.assertEqual(response.json(), expected_response)

    def test_retrieve_featured_products(self) -> None:
        featured_product_category = baker.make(
            "store.FeaturedProducts", header="test", make_m2m=True
        )

        url = reverse(
            "store:featured-product-detail", args=(featured_product_category.slug,)
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_response = FeaturedProductsReadOnlySerializer(
            StoreProductService.get_featured().first()
        ).data
        self.assertEqual(response.json(), expected_response)
