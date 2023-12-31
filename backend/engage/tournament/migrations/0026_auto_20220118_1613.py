# Generated by Django 3.1.1 on 2022-01-18 14:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournament', '0025_auto_20220118_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentprize',
            name='category',
            field=models.CharField(choices=[('free', 'Free'), ('subscribe', 'Subscriber')], max_length=10, null=True, verbose_name='Winner Category'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='free_open_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='open_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tournamentmatch',
            name='match_id',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='tournamentmatch',
            name='password',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='tournamentprize',
            name='prize',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tournamentprize',
            unique_together={('tournament', 'winner'), ('tournament', 'category', 'position')},
        ),
    ]
