# Generated by Django 3.1.4 on 2021-03-04 17:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0019_scraper_is_running'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='last_access',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='last access'),
        ),
    ]
