# Generated by Django 3.2.6 on 2021-09-16 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='html5game',
            name='game_type',
            field=models.CharField(choices=[('premium', 'Premium Game'), ('leisure', 'Leisure Game')], max_length=12, null=True),
        ),
    ]