# Generated by Django 3.1.4 on 2021-03-24 14:55

from django.db import migrations
import swp.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0026_user_is_error_recipient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='pdf_url',
            field=swp.models.fields.LongURLField(blank=True, max_length=1024, verbose_name='PDF URL'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='url',
            field=swp.models.fields.LongURLField(max_length=1024, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='scraper',
            name='start_url',
            field=swp.models.fields.LongURLField(max_length=1024, verbose_name='start URL'),
        ),
    ]
