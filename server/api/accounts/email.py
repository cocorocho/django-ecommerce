from djoser.email import (
    PasswordResetEmail as DjoserPasswordResetEmail
)


class PasswordResetEmail(DjoserPasswordResetEmail):
    template_name = "accounts/email/password_reset.html"
