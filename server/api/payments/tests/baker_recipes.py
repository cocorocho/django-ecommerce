from model_bakery.recipe import foreign_key, Recipe

from payments.models import Address


address = Recipe(
    _model=Address,
    country__slug="slug",
    city__slug="slug",
)

checkout = Recipe(
    _model="payments.checkout",
)
