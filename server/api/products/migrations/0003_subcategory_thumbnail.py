# Generated by Django 4.2.5 on 2023-09-28 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_category_name_alter_product_sku_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='thumbnails/sub-category/'),
        ),
    ]
