# Generated by Django 4.2.6 on 2023-10-17 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_description_rich'),
        ('store', '0005_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cart_items', to='products.product', verbose_name='Product'),
        ),
    ]