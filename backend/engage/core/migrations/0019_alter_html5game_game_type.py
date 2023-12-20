# Generated by Django 3.2.7 on 2021-09-29 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20210929_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='html5game',
            name='game_type',
            field=models.CharField(choices=[('free', 'Free Game'), ('premium', 'Premium Game')], max_length=12, null=True),
        ),
    ]