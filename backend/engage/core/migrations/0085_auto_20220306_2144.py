# Generated by Django 3.1.1 on 2022-03-06 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0084_auto_20220301_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='package',
            field=models.ManyToManyField(blank=True, to='core.Package', verbose_name='Package'),
        ),
    ]
