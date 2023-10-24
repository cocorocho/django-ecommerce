# Generated by Django 4.2.6 on 2023-10-20 13:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('store', '0008_cart_merged_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('name', models.CharField(blank=True, help_text='Ex: home, work', max_length=100, verbose_name='address name')),
                ('postal_code', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^[0-9]{6}$', 'Invalid postal code')], verbose_name='postal code')),
                ('address', models.CharField(max_length=500, verbose_name='address')),
                ('phone', models.CharField(blank=True, max_length=12, verbose_name='phone')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='addresses', to='cities_light.city', verbose_name='City')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='addresses', to='cities_light.country', verbose_name='Country')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='token')),
                ('checkout_complete', models.BooleanField(default=False, verbose_name='Checkout complete')),
                ('billing_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='billing_checkouts', to='payments.address', verbose_name='billing address')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='checkouts', to='store.cart', verbose_name='cart')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shipping_checkouts', to='payments.address', verbose_name='shipping address')),
            ],
            options={
                'verbose_name': 'Checkout',
                'verbose_name_plural': 'Checkouts',
            },
        ),
    ]
