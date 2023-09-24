from typing import Any
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    def create_user(self, username: str="", email: str | None = ..., password: str | None = ..., **extra_fields: Any) -> Any:
        if not username:
            username = email # type: ignore

        return super().create_user(username, email, password, **extra_fields)
