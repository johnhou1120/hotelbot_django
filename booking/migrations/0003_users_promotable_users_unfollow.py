# Generated by Django 4.0.6 on 2022-09-24 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='promotable',
            field=models.BooleanField(default=False, verbose_name='promotable'),
        ),
        migrations.AddField(
            model_name='users',
            name='unfollow',
            field=models.BooleanField(default=False, verbose_name='封鎖'),
        ),
    ]