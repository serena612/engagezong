# Generated by Django 3.2.7 on 2021-10-03 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_alter_mission_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='avatars/')),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.configuration')),
            ],
        ),
        migrations.AlterField(
            model_name='notifications',
            name='template',
            field=models.CharField(choices=[('home', 'Home Dashboard'), ('login', 'After Login'), ('christmas', 'Christmas'), ('easter', 'Easter'), ('instant', 'Instant')], max_length=40, null=True),
        ),
        migrations.DeleteModel(
            name='ProfileImage',
        ),
    ]
