# Generated by Django 4.2.6 on 2023-10-31 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_featuredproducts_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredproducts',
            name='slug',
            field=models.SlugField(default='a', editable=False),
            preserve_default=False,
        ),
    ]