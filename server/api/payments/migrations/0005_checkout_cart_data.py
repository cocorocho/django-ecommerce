# Generated by Django 4.2.6 on 2023-10-26 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_alter_address_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='cart_data',
            field=models.JSONField(editable=False, null=True),
        ),
    ]