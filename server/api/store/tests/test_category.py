from itertools import cycle

from rest_framework.reverse import reverse
from model_bakery import baker

from core.test import BaseTestCase
from products.models import Category, SubCategory
from store.models import StoreProduct
from store.serializers import StoreCategorySerializer, CategoryProductsSerializer


class TestEndpoints(BaseTestCase):
    def test_list_categories(self) -> None:
        URL = reverse("store:category-list")
        categories = baker.make(
            Category,
            _fill_optional=True,
            _quantity=5
        )
        sub_categories = baker.make(
            SubCategory,
            _quantity=20,
            category=cycle(categories)
        )
        
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        expected_data = StoreCategorySerializer(
            Category.objects.prefetch_related("sub_categories"),
            many=True
        ).data
        self.assertEqual(data, expected_data)

    def test_retrieve_category_products(self) -> None:
        category = baker.make_recipe("products.tests.category")
        products = baker.make_recipe(
            "store.tests.product",
            _quantity=50,
            product__sub_category__category=category
        )

        URL = reverse("store:category_products", args=[category.slug])
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)

        PAGINATION_SIZE = 20
        queryset = (
            StoreProduct.objects
                .select_related("product")
                .filter(product__sub_category__category=category)[:PAGINATION_SIZE]
        )
        expected_data = CategoryProductsSerializer(queryset, many=True).data

        self.assertEqual(
            response.json()["results"],
            expected_data
        )
