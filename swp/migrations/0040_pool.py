# Generated by Django 3.2.16 on 2023-12-04 12:20

from django.contrib.postgres.fields import CICharField
from django.db import migrations, models
from django.utils import timezone

from swp.utils.migrations import get_queryset

DEFAULT = 0


def create_default_pool(apps, schema_editor):
    get_queryset(apps, schema_editor, 'swp', 'Pool').get_or_create(id=DEFAULT, defaults={'name': 'Default'})


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0039_publication_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=timezone.now, editable=False, verbose_name='created')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('name', CICharField(max_length=50, unique=True, verbose_name='name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'pool',
                'verbose_name_plural': 'pools',
            },
        ),
        migrations.RunPython(
            code=create_default_pool,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AddField(
            model_name='thinktank',
            name='pool',
            field=models.ForeignKey(default=DEFAULT, on_delete=models.PROTECT, related_name='thinktanks', to='swp.pool', verbose_name='pool'),
            preserve_default=False,
        ),
    ]
