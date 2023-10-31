# Generated by Django 4.2.6 on 2023-10-30 19:30

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_featuredproducts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredproducts',
            name='header',
            field=tinymce.models.HTMLField(max_length=50, verbose_name='Featured items header'),
        ),
    ]
