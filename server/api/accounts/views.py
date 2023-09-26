from django.contrib.auth import login, logout

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from accounts.serializers import LoginSerializer


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request) -> Response: # type: ignore
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(request.data)
            login(request, user)

            return Response(
                serializer.data,
                status=HTTP_200_OK
            )
        

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request) -> Response:
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)
