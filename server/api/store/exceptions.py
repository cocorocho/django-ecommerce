from typing import Any

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import ValidationError


class InvalidCartProduct(ValidationError):
    """
    Raised when `cart` doesn't have given `Product` in its `CartItem(s)`
    """

    def __init__(self, detail=None, code=None):
        detail = "sslm"
        super().__init__(detail, code)


class IndeletableStore(DjangoValidationError):
    """
    Exception for attemting to delete store singleton
    """

    def __init__(self, message: Any = None, *args, **kwargs) -> None:
        message = _("Store can not be deleted")
        super().__init__(message, *args, **kwargs)
