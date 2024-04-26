# Generated by Django 3.1.4 on 2021-01-28 14:19

from django.contrib.postgres.fields import ArrayField
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0010_resolver_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='authors',
            field=ArrayField(base_field=models.CharField(max_length=255, blank=True), blank=True, null=True, size=None, verbose_name='authors'),
        ),
    ]
