# Generated by Django 4.0.3 on 2022-04-03 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.JSONField(max_length=50)),
                ('name', models.JSONField(max_length=50, null=True)),
                ('contact_number', models.JSONField(max_length=20, null=True)),
                ('lang', models.JSONField(choices=[('uz', 'Uzbek'), ('ru', 'Russian')], max_length=2, null=True)),
                ('verify', models.BooleanField(default=False)),
            ],
        ),
    ]
