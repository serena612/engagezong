# Generated by Django 3.2.7 on 2021-12-02 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator', '0021_auto_20211202_2353'),
        ('tournament', '0021_alter_tournamentprize_prize'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='operators',
        ),
        migrations.AddField(
            model_name='tournament',
            name='regions',
            field=models.ManyToManyField(to='operator.Region'),
        ),
    ]