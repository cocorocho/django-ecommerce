from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from cities_light.models import Country, Region

from core.base.serializers import DynamicFieldsModelSerializer
from payments.models import Checkout, Order, Address


class AddressSerializer(DynamicFieldsModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field="slug", queryset=Country.objects.all()
    )
    city = serializers.SlugRelatedField(
        slug_field="slug", queryset=Region.objects.all()
    )

    class Meta:
        model = Address
        fields = ("name", "country", "city", "postal_code", "address", "phone")

    def to_internal_value(self, data):
        _data = super().to_internal_value(data)
        _data["country"] = _data["country"].name
        _data["city"] = _data["city"].name

        return _data


class CheckoutReadOnlySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Checkout
        fields = ("token", "cart")
        read_only_fields = fields


class FinalizeOrderSerializer(serializers.ModelSerializer):
    shipping_address = AddressSerializer()
    billing_address = serializers.DictField(required=False)
    payment = serializers.DictField()

    def validate_payment(self, attrs):
        initial_data = self.initial_data
        use_shipping_addres_as_billing_address = attrs.get(
            "use_shipping_addres_as_billing_address"
        )

        if not use_shipping_addres_as_billing_address and initial_data.get(
            "billing_address", None
        ):
            raise serializers.ValidationError(_("billing address is required"))

        return attrs

    class Meta:
        model = Checkout
        fields = (
            "token",
            "shipping_address",
            "billing_address",
            "payment",
        )

    def update(self, instance, validated_data):
        shipping_address = validated_data.pop("shipping_address")
        payment_data = validated_data.get("payment")

        billing_address = None

        if payment_data and payment_data.get(
            "use_shipping_address_as_billing_address", False
        ):
            billing_address = shipping_address

        # print(validated_data)

        order = Order.objects.create(
            shipping_address=shipping_address, billing_address=billing_address
        )
        instance.order = order
        instance.checkout_complete = True

        return super().update(instance, validated_data)
