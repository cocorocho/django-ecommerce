# Generated by Django 4.2.6 on 2023-10-10 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_rich',
            field=models.TextField(blank=True, verbose_name='Description (WYSIWYG)'),
        ),
    ]
