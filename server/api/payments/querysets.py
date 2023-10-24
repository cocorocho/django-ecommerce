from __future__ import annotations
from datetime import timedelta

from django.utils import timezone
from django.db.models import F

from core.models import BaseQuerySet
from payments.constants import CHECKOUT_EXPIRE_AGE


class CheckoutQuerySet(BaseQuerySet):
    def valid(self) -> CheckoutQuerySet:
        """
        Validity of `Checkout` instance is determined by its `date_created`
        field and `CHECKOUT_EXPIRE_AGE`
        """
        return self.annotate(
            expire_date=(F("date_created") + timedelta(seconds=CHECKOUT_EXPIRE_AGE)),
        ).filter(expire_date__gte=timezone.now(), checkout_complete=False)
