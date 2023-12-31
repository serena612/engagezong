# Generated by Django 3.2.7 on 2021-10-11 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20211011_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='template',
            field=models.CharField(choices=[('instant', 'Instant One Time'), ('daily', 'Daily'), ('once_a_month', 'once_a_month'), ('home', 'When User Reach Home Dashboard'), ('login', 'After User Login'), ('how_to_use', 'How To Use Engage'), ('active_5_days', '5 Active Days After Joining'), ('active_10_days', '10 Active Days After Joining'), ('active_30_days', '30 Active Days After Joining'), ('user_register_for_tournament', 'User Registers For Tournament'), ('user_first_tournament', 'User Who Is First In Any Tournament'), ('user_second_third_tournament', 'Users Who Win A Prize (Second, Third ... etc)'), ('user_outside_the_winning_positions', 'User Outside The Winning Positions'), ('happy_birthday', 'Happy Birthday'), ('friend_added', 'Friend Added'), ('friend_remove', 'Friend Remove'), ('friend_request', 'Friend Request'), ('video_added', 'Video Added'), ('user_watch_video', 'If User Watches Any Video')], max_length=40, null=True),
        ),
    ]
