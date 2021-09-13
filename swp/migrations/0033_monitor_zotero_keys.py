# Generated by Django 3.1.4 on 2021-07-20 10:17

import django.contrib.postgres.fields
from django.db import migrations, models
from swp.models.fields import ZoteroKeyField


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0032_text_filter_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='zotero_keys',
            field=django.contrib.postgres.fields.ArrayField(base_field=ZoteroKeyField(), blank=True, default=list, help_text='{API_KEY}/(users|groups)/{USER_OR_GROUP_ID}/[collections/{COLLECTION_ID}/]items', size=None, verbose_name='Zotero keys'),
        ),
    ]
