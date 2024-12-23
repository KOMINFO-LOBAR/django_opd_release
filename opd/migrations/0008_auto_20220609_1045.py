# Generated by Django 3.2.6 on 2022-06-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opd', '0007_auto_20220609_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='judul_seo',
            field=models.SlugField(blank=True, default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='berita',
            name='judul_seo',
            field=models.SlugField(blank=True, default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='galery_foto',
            name='judul_seo',
            field=models.SlugField(blank=True, default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='page_rss',
            name='nama_seo',
            field=models.SlugField(blank=True, default='', unique=True),
        ),
        migrations.AlterField(
            model_name='page_widget',
            name='nama_seo',
            field=models.SlugField(blank=True, default='', unique=True),
        ),
        migrations.AlterField(
            model_name='pengumuman',
            name='judul_seo',
            field=models.SlugField(blank=True, default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='popup',
            name='judul_seo',
            field=models.SlugField(blank=True, default='', max_length=255, unique=True),
        ),
    ]
