from django.views.decorators.csrf import ensure_csrf_cookie
from django.http.response import HttpResponse, JsonResponse


@ensure_csrf_cookie
def set_csrf_token(request) -> HttpResponse:
    """
    Set CSRF Token
    """
    return JsonResponse({"status": "ok"})
