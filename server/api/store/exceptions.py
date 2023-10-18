from rest_framework.exceptions import ValidationError


class InvalidCartProduct(ValidationError):
    """
    Raised when `cart` doesn't have given `Product` in its `CartItem(s)`
    """
    def __init__(self, detail=None, code=None):
        detail = "sslm"
        super().__init__(detail, code)