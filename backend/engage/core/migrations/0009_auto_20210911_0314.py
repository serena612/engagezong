# Generated by Django 3.2.6 on 2021-09-11 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_game_support_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameapi',
            name='create_match',
        ),
        migrations.RemoveField(
            model_name='gameapi',
            name='create_tournament',
        ),
        migrations.RemoveField(
            model_name='gameapi',
            name='fetch_match_info',
        ),
        migrations.RemoveField(
            model_name='gameapi',
            name='fetch_player_info',
        ),
        migrations.RemoveField(
            model_name='gameapi',
            name='fetch_tournament_info',
        ),
        migrations.RemoveField(
            model_name='gameapi',
            name='response_mapping',
        ),
    ]
