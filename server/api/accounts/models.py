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
