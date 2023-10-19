# Generated by Django 4.2.6 on 2023-10-19 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_cartitem_unique_cart_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='merged_to',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='merged_with', to='store.cart', verbose_name='Merged carts'),
        ),
    ]
