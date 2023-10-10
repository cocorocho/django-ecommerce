from django.urls import path, include

from products.views.store import CategoryView, SubCategoryView, ProductView


app_name = "products"

urlpatterns = [
    path("<int:pk>/", ProductView.as_view(), name="store_product_details"),
    path("store/category/", CategoryView.as_view(), name="store_category"),
    path("store/category/<slug:slug>/", CategoryView.as_view(), name="store_category_retrieve"),
    path(
        "store/category/<slug:category_slug>/<slug:sub_category_slug>/",
        SubCategoryView.as_view(),
        name="store_product"
    ),
]