# Generated by Django 3.2.6 on 2021-08-18 13:43

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('action', models.CharField(choices=[('sign_up', 'On Sign Up'), ('ad_watch', 'On Ad Watch'), ('win_match', 'On Math Win'), ('win_tournament', 'On Tournament Win')], max_length=64, unique=True)),
                ('free_coins', models.PositiveIntegerField()),
                ('paid_coins', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission_rate', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('sponsor_tournament_cost', models.PositiveIntegerField(default=100)),
                ('disqualification_time', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('logo', models.ImageField(upload_to='games/icons/')),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='games/headers/')),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('base_url', models.URLField()),
                ('fetch_tournament_info', models.CharField(max_length=128, null=True)),
                ('fetch_match_info', models.CharField(max_length=128, null=True)),
                ('fetch_player_info', models.CharField(max_length=128, null=True)),
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.game')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
