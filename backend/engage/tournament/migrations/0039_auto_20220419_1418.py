# Generated by Django 3.1.1 on 2022-04-19 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0038_auto_20220412_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='label_next_time',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Label Next to Time'),
        ),
    ]
