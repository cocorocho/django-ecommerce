from itertools import cycle

from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_200_OK
)
from model_bakery import baker

from core.test import BaseTestCase
from store.models.cart import CartItem, Cart
from store.serializers import CartSerializer, CartWriteUpdateSerializer


class TestCartModel(BaseTestCase):
    def test_session_id_generation(self) -> None:
        """
        Test generation of `session_id` when creating a `Cart` instance
        """
        from store.constants import CART_SESSION_ID_LEN

        cart = baker.make_recipe("store.tests.cart")
        self.assertTrue(
            isinstance(cart.session_id, str)
        )
        self.assertTrue(
            len(cart.session_id) == CART_SESSION_ID_LEN
        )
    

class TestCartEndpoints(BaseTestCase):
    def test_list_carts_returns_http_405(self) -> None:
        url = reverse("store:cart-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_cart_without_products(self) -> None:
        url = reverse("store:cart-list")
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, HTTP_201_CREATED
        )

    def test_create_cart_with_products(self) -> None:
        products = baker.make_recipe("products.tests.product", _quantity=4)

        payload = {
            "items": [
                {"product": products[0].pk, "quantity": 4},
                {"product": products[1].pk, "quantity": 5},
                {"product": products[2].pk}, # No quantity, should be 1 as default
                {"product": products[3].pk, "quantity": 6},
            ]
        }

        url = reverse("store:cart-list")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), len(payload["items"]))
        self.assertEqual(
            CartWriteUpdateSerializer(Cart.objects.first()).data,
            response.json()
        )

    def test_create_cart_with_invalid_product_returns_http_400(self) -> None:
        payload = {
            "items": [
                {"product": 999}
            ]
        }

        url = reverse("store:cart-list")
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertFalse(CartItem.objects.exists())

    def test_update_cart(self) -> None:
        cart = baker.make_recipe("store.tests.cart")
        products = baker.make_recipe("products.tests.product", _quantity=1)
        cart_items = baker.make_recipe("store.tests.cart_item", cart=cart, _quantity=1, product=cycle(products))

        new_product = baker.make_recipe("products.tests.product")

        updated_items = [
            {
                # Add New cart item here
                "product": new_product.pk,
                "quantity": 55
            },
            {
                # Update existing
                "id": cart_items[0].pk,
                "product": cart_items[0].product.pk,
                "quantity": 60
            }
            # Delete rest
        ]
        payload = {"items": updated_items}
        url = reverse("store:cart-detail", args=(cart.session_id,))
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            CartItem.objects.count(),
            len(updated_items)
        )
        self.assertTrue(
            CartItem.objects.filter(product__pk__in=[new_product.pk, products[0].pk]).exists()
        )
        for updated_item in updated_items:
            self.assertEqual(
                CartItem.objects.get(
                    product__pk=updated_item["product"]
                ).quantity,
                updated_item["quantity"]
            )
        
    def test_add_product_to_empty_cart(self) -> None:
        cart = baker.make_recipe("store.tests.cart")
        products = baker.make_recipe("products.tests.product", _quantity=2)

        url = reverse("store:cart-add-product", args=(cart.session_id,))
        quantity = 16
        payload = {"product": products[0].pk, "quantity": quantity}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(
            cart.items.filter(product__pk=products[0].pk, quantity=quantity).exists()
        )
    
    def test_add_new_product_to_cart_with_items(self) -> None:
        cart = baker.make_recipe("store.tests.cart")
        # 4 Products total, 3 in cart already
        products = baker.make_recipe("products.tests.product", _quantity=4)
        cart_items = baker.make_recipe(
            "store.tests.cart_item",
            cart=cart, product=cycle(products),
            _quantity=3
        )

        product_to_add = products[-1]
        url = reverse("store:cart-add-product", args=(cart.session_id,))
        payload = {"product": product_to_add.pk}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(
            cart.items.filter(product__pk__in=[product.pk for product in products]).count(),
            4
        )


    def test_add_existing_product_to_cart(self) -> None:
        """
        Test cart item quantity when product already exists in cart
        """
        cart = baker.make_recipe("store.tests.cart")
        product = baker.make_recipe("products.tests.product")
        cart_item = baker.make_recipe(
            "store.tests.cart_item",
            cart=cart, product=product
        )

        initial_quantity = cart_item.quantity
        url = reverse("store:cart-add-product", args=(cart.session_id,))
        payload = {"product": product.pk}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Validate quantity
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 2)
    
    def test_update_product_quantity(self) -> None:
        cart = baker.make_recipe("store.tests.cart")
        product = baker.make_recipe("products.tests.product")
        cart_item = baker.make_recipe(
            "store.tests.cart_item",
            cart=cart, product=product
        )
        new_quantity = 60
        
        payload = {
            "product": product.pk,
            "quantity": new_quantity
        }

        url = reverse("store:cart-product-update-delete", args=(cart.session_id, cart_item.pk))
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            cart.items.get(product=product).quantity,
            new_quantity
        )
        
    def test_delete_product_from_cart(self) -> None:
        cart = baker.make_recipe("store.tests.cart")
        products = baker.make_recipe("products.tests.product", _quantity=5)
        cart_items = baker.make_recipe(
            "store.tests.cart_item",
            cart=cart,
            product=cycle(products),
            _quantity=5
        )
        cart_item_to_delete = cart_items[0]

        url = reverse("store:cart-product-update-delete", args=(cart.session_id, cart_item_to_delete.pk))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertFalse(
            CartItem.objects.filter(pk=cart_item_to_delete.pk).exists()
        )

    def test_update_cart_item_quantity(self) -> None:
        cart = baker.make_recipe("store.tests.cart")
        product = baker.make_recipe("products.tests.product")
        cart_item = baker.make_recipe(
            "store.tests.cart_item",
            cart=cart, product=product
        )

        url = reverse("store:cart-product-update-delete", args=(cart.session_id, cart_item.pk))
        quantities = [
            {
                "value": 3,
                "expected_value": 3,
                "expected_status": HTTP_200_OK
            },
            {
                "value": -1,
                "expected_status": HTTP_400_BAD_REQUEST
            }
        ]
        for quantity in quantities:
            payload = {"quantity": quantity["value"]}
            response = self.client.patch(url, payload)
            self.assertEqual(response.status_code, quantity["expected_status"])
            expected_value = quantity.get("expected_value")
            if expected_value:
                cart_item.refresh_from_db()
                self.assertEqual(cart_item.quantity, expected_value)
