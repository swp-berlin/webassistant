# Generated by Django 3.2.16 on 2023-12-12 10:59

from collections import defaultdict

from django.db import migrations, models

from swp.models.choices import FilterField
from swp.utils.migrations import get_queryset

TRANSLATION_FIELDS = [
    'title',
    'subtitle',
    'abstract',
]

AND = ' AND '.join
OR = ' OR '.join


def build_queries(apps, schema_editor):
    queryset = get_queryset(apps, schema_editor, 'swp', 'Monitor')
    monitors = queryset.prefetch_related('thinktank_filters__publication_filters')

    for monitor in monitors:
        thinktanks = defaultdict(list)

        for thinktank_filter in monitor.thinktank_filters.all():
            if filters := thinktank_filter.publication_filters.all():
                thinktanks[thinktank_filter.thinktank_id].append(filters)
            else:
                thinktanks[thinktank_filter.thinktank_id].extend([])

        monitor.query = get_query(thinktanks)

    queryset.bulk_update(monitors, fields=['query'])


def get_query(thinktanks):
    return OR(
        get_thinktank(thinktank, thinktanks[thinktank])
        for thinktank in sorted(thinktanks)
    )


def get_thinktank(thinktank, publication_filters):
    thinktank = f'thinktank.id:{thinktank}'

    if publication_filters:
        filters = OR(
            get_thinktank_filter(publication_filter)
            for publication_filter in publication_filters
        )

        return f'({thinktank} AND ({filters}))'

    return thinktank


def get_thinktank_filter(publication_filters):
    return AND(
        get_publication_filter(publication_filter)
        for publication_filter in publication_filters
    )


def get_publication_filter(publication_filter):
    return get_filter(publication_filter.field, publication_filter.values)


def get_filter(field, values):
    if field == FilterField.TEXT:
        fields = OR(get_filter(field, values) for field in TRANSLATION_FIELDS)

        return f'({fields})'

    if field in TRANSLATION_FIELDS:
        field = rf'{field}.\*'

    if len(values) == 1:
        return f'{field}:%s' % quote(*values)

    values = OR(quote(value) for value in values)

    return f'{field}:({values})'


def quote(value):
    if any(map(str.isspace, value)):
        return f'"{value}"'

    return value


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0043_monitor_pool'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='query',
            field=models.TextField(blank=True, default='', verbose_name='query'),
            preserve_default=False,
        ),
        migrations.RunPython(
            code=build_queries,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='thinktankfilter',
            name='monitor',
        ),
        migrations.RemoveField(
            model_name='thinktankfilter',
            name='thinktank',
        ),
        migrations.DeleteModel(
            name='PublicationFilter',
        ),
        migrations.DeleteModel(
            name='ThinktankFilter',
        ),
    ]
