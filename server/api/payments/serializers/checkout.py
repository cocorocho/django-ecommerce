from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import HttpRequest

from rest_framework import serializers
from cities_light.models import Country, Region

from core.base.serializers import DynamicFieldsModelSerializer
from payments.models import Checkout, Order, Address
from store.serializers import CartDetailsReadOnlySerializer


class AddressKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get("request")
        user = request.user

        return Address.objects.filter(user=user)


class AddressField(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, dict):
            # Address is passed as a dict, validate
            serializer = AddressCreateUpdateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return serializer.data
        elif isinstance(data, str):
            # Address is passed as pk
            try:
                address = Address.objects.get(pk=data)
                serializer = AddressCreateUpdateSerializer(address)
                return serializer.data
            except Address.DoesNotExist:
                raise serializers.ValidationError("Address does not exist")

        raise serializers.ValidationError("Invalid address")


class AddressSerializer(DynamicFieldsModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field="name", queryset=Country.objects.all()
    )
    city = serializers.SlugRelatedField(
        slug_field="name", queryset=Region.objects.all()
    )

    class Meta:
        model = Address
        fields = (
            "id",
            "name",
            "country",
            "city",
            "postal_code",
            "address",
            "phone",
            "user",
        )
        read_only_fields = fields


class AddressCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=False,
        queryset=get_user_model().objects.all(),
    )
    country = serializers.SlugRelatedField(
        slug_field="slug", queryset=Country.objects.all()
    )
    city = serializers.SlugRelatedField(
        slug_field="slug", queryset=Region.objects.all()
    )

    class Meta:
        model = Address
        fields = (
            "id",
            "name",
            "country",
            "city",
            "postal_code",
            "address",
            "phone",
            "user",
        )
        read_only_fields = ("id",)

    def to_internal_value(self, data):
        _data = super().to_internal_value(data)
        _data["country"] = _data["country"].name
        _data["city"] = _data["city"].name

        return _data


class CheckoutReadOnlySerializer(DynamicFieldsModelSerializer):
    cart = CartDetailsReadOnlySerializer(read_only=False)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Checkout
        fields = ("token", "cart", "total_price")
        read_only_fields = fields


class FinalizeOrderSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    shipping_address = AddressCreateUpdateSerializer(allow_null=True, required=False)
    shipping_address_id = AddressKeyRelatedField(allow_null=True, required=False)
    billing_address = serializers.DictField(required=False)
    payment = serializers.DictField()

    def _validate_email(self, request: HttpRequest, email: str | None) -> None:
        if not request.user.is_authenticated and not email:
            raise serializers.ValidationError(_("Email is required"))

    def _validate_shipping_address(self, request: HttpRequest, attrs: dict) -> None:
        address = attrs.get("shipping_address")
        address_from_id = attrs.get("shipping_address_id")

        if not address_from_id and not address:
            raise serializers.ValidationError(
                {"shipping_address": _("address is required")}
            )

    def validate(self, attrs: dict) -> dict:
        request = self.context.get("request")
        email = attrs.get("email")

        self._validate_email(request, email)
        self._validate_shipping_address(request, attrs)

        return attrs

    def validate_payment(self, attrs):
        initial_data = self.initial_data
        use_shipping_address_as_billing_address = attrs.get(
            "use_shipping_address_as_billing_address"
        )

        if not use_shipping_address_as_billing_address and not initial_data.get(
            "billing_address", None
        ):
            raise serializers.ValidationError(_("billing address is required"))

        return attrs

    def validate_shipping_address(self, attrs):
        return attrs

    class Meta:
        model = Checkout
        fields = (
            "token",
            "shipping_address",
            "shipping_address_id",
            "billing_address",
            "payment",
            "email",
        )

    def update(self, instance, validated_data):
        billing_address = None
        shipping_address = validated_data.pop("shipping_address", None)

        shipping_address_from_id = validated_data.pop("shipping_address_id", None)
        if shipping_address_from_id:
            shipping_address = AddressCreateUpdateSerializer(
                shipping_address_from_id
            ).data

        payment_data = validated_data.get("payment")

        if payment_data and payment_data.get(
            "use_shipping_address_as_billing_address", False
        ):
            billing_address = shipping_address

        order = Order.objects.create(
            shipping_address=shipping_address,
            billing_address=billing_address,
        )
        instance.order = order
        instance.checkout_complete = True

        return super().update(instance, validated_data)
