# Generated by Django 4.0.3 on 2022-04-22 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_address_order_shipping_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('process', 'Process'), ('cancelled', 'Cancelled'), ('delivered', 'Delivered')], default='active', max_length=10),
        ),
    ]