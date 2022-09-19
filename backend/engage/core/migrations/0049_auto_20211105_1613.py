# Generated by Django 3.2.7 on 2021-11-05 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_alter_notifications_template'),
    ]

    operations = [
        migrations.RenameField(
            model_name='featuredgame',
            old_name='mobile_url',
            new_name='android_link',
        ),
        migrations.RenameField(
            model_name='featuredgame',
            old_name='pc_url',
            new_name='ios_link',
        ),
        migrations.RemoveField(
            model_name='game',
            name='mobile_link',
        ),
        migrations.AddField(
            model_name='featuredgame',
            name='pc_link',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='android_link',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='ios_link',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='pc_link',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]