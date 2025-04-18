# Generated by Django 4.0.10 on 2024-10-17 12:37

from django.contrib.postgres.fields import CICharField
from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0051_char_array_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=timezone.now, editable=False, verbose_name='created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('name', CICharField(max_length=50, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.AddField(
            model_name='publication',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='publications', to='swp.category', verbose_name='categories'),
        ),
        migrations.AddField(
            model_name='scraper',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='scrapers', to='swp.category', verbose_name='categories'),
        ),
    ]
