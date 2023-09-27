from django.contrib.auth import login, logout
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest
from django.utils.crypto import get_random_string

from rest_framework.response import Response


AUTH_COOKIE_KEY = "authenticated"


def login_user(request: HttpRequest, user: AbstractBaseUser, response: Response) -> Response:
    """
    Uses django's `login` method and adds not-httponly cookie for client-side
    to determine if user is authenticated

    :param Response response: Response instance for setting cookie
    """
    login(request, user)

    cookie_value = get_random_string(4) # Cookie value is random string but has no meaning
    response.set_cookie(
        AUTH_COOKIE_KEY,
        cookie_value    
    )
    
    return response


def logout_user(request: HttpRequest, response: Response):
    logout(request)
    
    response.delete_cookie(AUTH_COOKIE_KEY)
    
    return response
