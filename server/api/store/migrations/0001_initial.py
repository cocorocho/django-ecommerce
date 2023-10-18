# Generated by Django 4.2.6 on 2023-10-10 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.models.cart


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('session_id', models.CharField(default=store.models.cart.generate_cart_session_id, editable=False, max_length=8)),
                ('check_out_complete', models.BooleanField(default=False, verbose_name='Checked Out')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Item quantity')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='store.cart', verbose_name='Cart')),
            ],
            options={
                'verbose_name': 'Cart item',
                'verbose_name_plural': 'Cart items',
            },
        ),
    ]
