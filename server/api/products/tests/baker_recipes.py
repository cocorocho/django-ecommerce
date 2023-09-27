from itertools import cycle

from model_bakery.recipe import Recipe, foreign_key

from products.models import Category, SubCategory, Product


CATEGORY_NAMES = (
    "Knives",
    "Swords",
    "Axes",
    "Machetes"
)

SUB_CATEGORY_NAMES = (
    "Survival Knives",
    "Hunting Knives",
    "Neck Knives",
    "Nordic Knives",
    "Daggers"
)

PRODUCT_NAMES = (
    "Avant",
    "Attaboy",
    "Bombastic",
    "Fighter",
    "Bamboo"
)

category = Recipe(
    _model=Category,
    # name=cycle(CATEGORY_NAMES)
)

sub_category = Recipe(
    _model=SubCategory,
    category=foreign_key(category, one_to_one=True),
    # name=cycle(SUB_CATEGORY_NAMES)
)

product = Recipe(
    _model=Product,
    manufacturer="CRKT",
    # name=cycle(PRODUCT_NAMES),
    sub_category=foreign_key(sub_category),
    attributes=[]
)
