# Generated by Django 3.2.7 on 2021-12-02 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator', '0021_auto_20211202_2353'),
        ('core', '0060_battlepass_unlock_vip_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='html5game',
            name='supported_operators',
        ),
        migrations.AddField(
            model_name='html5game',
            name='regions',
            field=models.ManyToManyField(to='operator.Region'),
        ),
        migrations.AlterField(
            model_name='battlepass',
            name='unlock_vip_cost',
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True, verbose_name='Unlock VIP price'),
        ),
    ]
