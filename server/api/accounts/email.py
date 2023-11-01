from djoser.email import PasswordResetEmail as DjoserPasswordResetEmail
from store.models import Store


class PasswordResetEmail(DjoserPasswordResetEmail):
    template_name = "accounts/email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        store_name = Store.get_store_name()
        context["store_name"] = store_name
        return context
