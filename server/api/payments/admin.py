from django.contrib import admin

from payments.models import Order, Address


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["shipping_address"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
