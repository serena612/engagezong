# Generated by Django 3.1.1 on 2022-01-18 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0051_auto_20220110_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_seen',
        ),
    ]
