# Generated by Django 3.2.6 on 2021-09-11 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator', '0008_auto_20210911_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='is_access_premium_games',
            field=models.BooleanField(default=True, verbose_name='Has access to premium games'),
        ),
    ]