# Generated by Django 4.2.5 on 2023-09-27 20:17

from django.db import migrations, models
import django.db.models.deletion
import django_jsonform.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('name', models.CharField(max_length=100, verbose_name='Product Category')),
                ('slug', models.SlugField(editable=False)),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('name', models.CharField(max_length=50, verbose_name='Sub Category')),
                ('slug', models.SlugField(editable=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='products.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Sub Category',
                'verbose_name_plural': 'Sub Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('sku', models.CharField(max_length=100, verbose_name='Product SKU')),
                ('manufacturer', models.CharField(max_length=100, verbose_name='Manufacturer')),
                ('name', models.CharField(max_length=100, verbose_name='Product Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('attributes', django_jsonform.models.fields.JSONField(verbose_name='Product attributes')),
                ('slug', models.SlugField(editable=False)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.subcategory', verbose_name='Sub Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]