# Generated by Django 3.1.4 on 2021-01-19 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0010_resolver_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraper',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
    ]
