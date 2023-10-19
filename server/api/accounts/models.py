from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from store.models.cart import Cart

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager
from core.models import BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(verbose_name=_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def cart(self) -> "Cart":
        """
        Get active cart for user
        """
        try:
            return self.carts.active_carts().latest("pk")
        except self.carts.model.DoesNotExist:
            return self.carts.create(user=self)

    @property
    def has_cart(self) -> bool:
        """
        Check if user has a an active, not abandoned cart
        """
        return self.carts.active_carts().exists()
