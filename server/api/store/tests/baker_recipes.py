from model_bakery.recipe import Recipe, foreign_key

from store.models import StoreProduct


product = Recipe(
    _model=StoreProduct,
    product=foreign_key("products.tests.product", one_to_one=True)
)