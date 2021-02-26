from django.db import migrations
import swp.models.fields
from swp.models.choices import ResolverType, DataResolverKey


TYPE_MAP = {
    DataResolverKey.TITLE.value: ResolverType.TITLE.value,
    DataResolverKey.SUBTITLE.value: ResolverType.SUBTITLE.value,
    DataResolverKey.ABSTRACT.value: ResolverType.ABSTRACT.value,
    DataResolverKey.PUBLICATION_DATE.value: ResolverType.PUBLICATION_DATE.value,
    DataResolverKey.URL.value: ResolverType.URL.value,
}

TAG_TYPE_MAP = {
    'TagData': ResolverType.DATA.value,
    'TagAttribute': ResolverType.ATTRIBUTE.value,
    'TagStatic': ResolverType.STATIC.value,
}


def replace_old_config(config):
    if isinstance(config, list):
        for c in config:
            replace_old_config(c)

        return

    type = config.get('type')
    key = config.get('key')

    if type in [ResolverType.DATA, ResolverType.ATTRIBUTE, ResolverType.STATIC] and key in TYPE_MAP:
        resolver = {**config}
        del resolver['key']

        config.clear()

        config['type'] = TYPE_MAP[key]
        config['resolver'] = resolver

        return

    if type == 'Tag':
        replace_tag_config(config)

    if isinstance(config, dict):
        for k, v in config.items():
            if isinstance(v, (list, dict)):
                replace_old_config(v)


def replace_tag_config(config):
    type = config['resolver']['type']

    config['type'] = ResolverType.TAGS.value
    config['resolver']['type'] = TAG_TYPE_MAP[type]


def migrate_config(apps, schema_editor):
    Scraper = apps.get_model('swp', 'Scraper')

    scrapers = Scraper.objects.all()

    for scraper in scrapers:
        replace_old_config(scraper.data)
        scraper.save()


class Migration(migrations.Migration):
    dependencies = [
        ('swp', '0016_authors_resolver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationfilter',
            name='field',
            field=swp.models.fields.ChoiceField(
                choices=[('title', 'Title'), ('subtitle', 'Subtitle'), ('abstract', 'Abstract'),
                         ('authors', 'Authors'), ('publication_date', 'Publication Date'), ('url', 'URL'),
                         ('pdf_url', 'PDF URL'), ('tags', 'Tags')], db_index=True, default='title', max_length=16,
                verbose_name='field'),
        ),
        migrations.RunPython(code=migrate_config, reverse_code=migrations.RunPython.noop),
    ]
