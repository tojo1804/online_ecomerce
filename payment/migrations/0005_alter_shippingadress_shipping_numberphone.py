# Generated by Django 5.1.3 on 2024-11-30 15:48

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_shippingadress_shipping_numberphone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingadress',
            name='shipping_numberphone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
