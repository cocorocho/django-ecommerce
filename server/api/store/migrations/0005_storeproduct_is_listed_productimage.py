# Generated by Django 4.2.5 on 2023-09-29 15:34

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_storeproduct_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeproduct',
            name='is_listed',
            field=models.BooleanField(default=True, verbose_name='Listed for sale'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('image', models.ImageField(upload_to=store.models.product_image_upload_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.storeproduct')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
    ]