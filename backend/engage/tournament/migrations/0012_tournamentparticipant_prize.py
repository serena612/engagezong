# Generated by Django 3.2.7 on 2021-10-11 02:48

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0011_auto_20210916_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentparticipant',
            name='prize',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]