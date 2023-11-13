from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class StorePolicies(models.Model):
    """
    Abstract model for Store Policies
    """

    return_policy = RichTextField(
        blank=True,
        verbose_name="Return policy",
    )
    shipping_policy = RichTextField(
        blank=True,
        verbose_name=_("Shipping policy"),
    )
    tos = RichTextField(
        blank=True,
        verbose_name=_("Terms of service"),
    )
    privacy_policy = RichTextField(
        blank=True,
        verbose_name=_("Privacy policy"),
    )

    class Meta:
        abstract = True


class Socials(models.Model):
    """
    Social media urls for store
    """

    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)

    class Meta:
        abstract = True


class SEO(models.Model):
    """
    SEO properties for store
    """

    description = models.CharField(
        max_length=150,
        verbose_name=_("Store description"),
        help_text=_("Page description for SEO"),
        blank=True,
    )

    class Meta:
        abstract = True
