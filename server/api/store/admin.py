from django.utils.translation import gettext_lazy as _

from django.contrib import admin

from store.models.abstract import StorePolicies, Socials
from store.models import FeaturedProducts, Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ["name", "logo", "favicon", "address"]}),
        (
            _("Policies"),
            {"fields": [field.name for field in StorePolicies._meta.fields]},
        ),
        (_("Socials"), {"fields": [field.name for field in Socials._meta.fields]}),
    )


@admin.register(FeaturedProducts)
class FeaturedProductsAdmin(admin.ModelAdmin):
    pass
