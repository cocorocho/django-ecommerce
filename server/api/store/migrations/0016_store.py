# Generated by Django 4.2.6 on 2023-10-31 19:16

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_featuredproducts_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Date modified')),
                ('_singleton', models.BooleanField(default=True, editable=False, unique=True)),
                ('return_policy', ckeditor.fields.RichTextField(blank=True, verbose_name='Return policy')),
                ('shipping_policy', ckeditor.fields.RichTextField(blank=True, verbose_name='Shipping policy')),
                ('tos', ckeditor.fields.RichTextField(blank=True, verbose_name='Terms of service')),
                ('privacy_policy', ckeditor.fields.RichTextField(blank=True, verbose_name='Privacy policy')),
                ('instagram', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('name', models.CharField(default='My Store', max_length=100, verbose_name='Store name')),
                ('logo', models.ImageField(upload_to='store', verbose_name='Store logo')),
                ('favico', models.ImageField(blank=True, null=True, upload_to='store', verbose_name='Favicon')),
                ('address', models.CharField(blank=True, max_length=500, verbose_name='address')),
            ],
            options={
                'verbose_name': 'Store Info',
                'verbose_name_plural': 'Store Info',
            },
        ),
    ]