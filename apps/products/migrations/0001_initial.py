# Generated by Django 4.0.3 on 2022-04-03 13:57

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.JSONField()),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='products.category.txt')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('title', models.JSONField()),
                ('image', models.ImageField(null=True, upload_to=products.models.upload_to)),
                ('desc', models.JSONField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category.txt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.category.txt')),
            ],
        ),
    ]
