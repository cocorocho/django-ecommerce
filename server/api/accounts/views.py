from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from accounts.serializers import LoginSerializer
from accounts.services.auth import login_user, logout_user
from store.services.cart import merge_user_cart_with_client_cart
from payments.models import Address
from payments.serializers.checkout import (
    AddressSerializer,
    AddressCreateUpdateSerializer,
)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request) -> Response:  # type: ignore
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(request.data)
            response = Response(serializer.data, status=HTTP_200_OK)
            login_user(request, user, response)

            # Attempt merge, create new cart, set cookie if required
            merge_user_cart_with_client_cart(request, response)

            return response


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request) -> Response:
        response = Response(status=HTTP_204_NO_CONTENT)
        logout_user(request, response)
        return response


class UserAddressViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AddressCreateUpdateSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        return Address.objects.select_related("user", "city", "country").filter(
            user=self.request.user
        )
