# Generated by Django 3.2.6 on 2021-09-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator', '0013_delete_operatorevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='operatorhomesection',
            name='icon',
            field=models.ImageField(null=True, upload_to='section/icons'),
        ),
    ]
