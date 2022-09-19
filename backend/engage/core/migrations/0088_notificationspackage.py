# Generated by Django 3.1.1 on 2022-04-03 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0087_auto_20220321_2142'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationsPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('notification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.notifications')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.package', verbose_name='Package')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]