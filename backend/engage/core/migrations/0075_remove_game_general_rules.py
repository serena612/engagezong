# Generated by Django 3.1.1 on 2022-01-18 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_auto_20220114_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='general_rules',
        ),
    ]
