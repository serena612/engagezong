# Generated by Django 3.2.7 on 2021-11-22 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operator', '0018_auto_20211122_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operator',
            name='is_access_premium_games',
        ),
        migrations.RemoveField(
            model_name='operator',
            name='supported_games',
        ),
    ]
