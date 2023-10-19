from model_bakery.recipe import Recipe, foreign_key

from store.models.cart import Cart, CartItem


cart = Recipe(_model=Cart)

cart_item = Recipe(
    _model=CartItem,
    cart=foreign_key(cart),
    product=foreign_key("products.tests.product", one_to_one=True),
)
