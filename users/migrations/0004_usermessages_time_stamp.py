# Generated by Django 3.2.21 on 2023-09-22 14:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230922_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessages',
            name='time_stamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
