from itertools import cycle

from model_bakery.recipe import Recipe, foreign_key

from products.models import Category, SubCategory, Product


CATEGORIES = {
    "guitars": [
        "electric guitars",
        "classical guitars",
        "acoustic guitars"
    ],
    "drums": [
        "acoustic drums",
        "electronic drums",
        "cymbals"
    ],
    "keys": [
        "keyboards",
        "pianos",
        "electric ograns"
    ]
}

category = Recipe(
    _model=Category,
    name=cycle(i for i in CATEGORIES.keys())
)

sub_category = Recipe(
    _model=SubCategory,
    category=foreign_key(category)
)

product = Recipe(
    _model=Product,
    sub_category=foreign_key(sub_category)
)
