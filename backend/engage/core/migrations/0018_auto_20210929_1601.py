# Generated by Django 3.2.7 on 2021-09-29 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_notifications'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifications',
            options={'verbose_name': 'Notification', 'verbose_name_plural': 'Notifications'},
        ),
        migrations.AlterField(
            model_name='notifications',
            name='template',
            field=models.CharField(choices=[('home', 'Home Dashboard'), ('login', 'After Login'), ('christmas', 'Christmas'), ('easter', 'Easter')], max_length=40, null=True),
        ),
    ]