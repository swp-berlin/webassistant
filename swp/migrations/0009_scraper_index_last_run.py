# Generated by Django 3.1.4 on 2021-01-06 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0008_delete_scrapertype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scraper',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'activate', 'deactivate'), 'get_latest_by': 'last_run', 'verbose_name': 'scraper', 'verbose_name_plural': 'scrapers'},
        ),
        migrations.AlterModelManagers(
            name='scraper',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='thinktank',
            managers=[
            ],
        ),
        migrations.AddIndex(
            model_name='scraper',
            index=models.Index(fields=['-last_run'], name='swp_scraper_last_ru_81bc24_idx'),
        ),
    ]