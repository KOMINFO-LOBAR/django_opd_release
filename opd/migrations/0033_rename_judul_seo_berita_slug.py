# Generated by Django 4.2 on 2025-01-23 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opd', '0032_auto_20240927_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='berita',
            old_name='judul_seo',
            new_name='slug',
        ),
    ]
