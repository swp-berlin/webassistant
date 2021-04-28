# Generated by Django 3.1.4 on 2021-03-25 13:40

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0027_long_url_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None, verbose_name='tags'),
        ),
    ]