from django.contrib import admin

from store.models import FeaturedProducts


@admin.register(FeaturedProducts)
class FeaturedProductsAdmin(admin.ModelAdmin):
    pass
