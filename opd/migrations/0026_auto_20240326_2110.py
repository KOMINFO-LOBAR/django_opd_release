# Generated by Django 3.2.8 on 2024-03-26 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opd', '0025_weather'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='jam',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='lon',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='weather',
            name='tgl',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]