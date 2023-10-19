from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from accounts.serializers import LoginSerializer
from accounts.services.auth import login_user, logout_user
from store.services.cart import merge_user_cart_with_client_cart


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
