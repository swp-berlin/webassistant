import re
from argparse import ArgumentParser
from itertools import chain

from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction, IntegrityError
from django.utils import timezone

from cosmogo.utils.requests import TimeOutSession

from swp.models import Monitor, ZoteroTransfer, Publication
from swp.utils.zotero import build_zotero_api_url, get_zotero_api_headers, OBJECT_KEY_ALPHABET


PUB_ID_BASE33 = re.compile('^(?P<base_33>.*)(S|SW|SWP|SWPZ|SWPZT|SWPZTA|SWPZTAP|SWPZTAPI)$')

# see https://www.zotero.org/support/dev/web_api/v3/basics#total_results
MAX_ITEMS_PER_REQUEST = 100


def get_publication_id(key: str):
    match = PUB_ID_BASE33.match(key)

    if not match:
        return None

    id_base_33 = match.group('base_33')
    length = len(id_base_33)

    pub_id = 0

    for idx, val in enumerate(id_base_33):
        pub_id += OBJECT_KEY_ALPHABET.index(val) * 33**(length - idx - 1)

    if pub_id > 2147483647:
        # max value for primary key field
        return None

    return pub_id


class Command(BaseCommand):

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('--dry_run', dest='dry_run', action='store_true',  default=False)

    def handle(self, **kwargs):
        zotero_keys = chain(*Monitor.objects.filter(zotero_keys__len__gt=0).values_list('zotero_keys', flat=True))
        zotero_infos = {
            (api_key, path) for api_key, path, _ in [
                Monitor.get_zotero_info(zotero_key) for zotero_key in zotero_keys
            ]
        }

        now = timezone.now()
        created = 0
        updated = 0

        with transaction.atomic():
            for api_key, path in zotero_infos:
                url = f'{build_zotero_api_url(path)}?itemType=book&limit={MAX_ITEMS_PER_REQUEST}'
                headers = get_zotero_api_headers(api_key)

                session = TimeOutSession(settings.ZOTERO_API_TIMEOUT)

                attachments = self.get_attachments(api_key, path)

                while url:
                    response = session.request('GET', url, headers=headers)

                    next = response.links.get('next')
                    url = next and next.get('url')

                    for item in response.json():
                        zotero_key = item.get('key')

                        if not zotero_key:
                            self.stderr.write(
                                f'API_KEY: {api_key}, PATH: {path}. '
                                f'Item doesn\'t contain zotero key: {item}'
                            )
                            continue

                        publication_id = get_publication_id(zotero_key)

                        if not publication_id:
                            self.stderr.write(
                                f'API_KEY: {api_key}, PATH: {path}. '
                                f'Item with key {zotero_key} doesn\'t match pattern'
                            )
                            continue

                        data = item.get('data')

                        title = data.get('title')
                        collection_keys = data.get('collections')
                        version = data.get('version')
                        date_added = data.get('dateAdded')
                        date_modified = data.get('dateModified')

                        try:
                            publication = Publication.objects.get(pk=publication_id)

                            if publication.title != title:
                                # Caution! This might not be our publication. We will ignore it.
                                continue

                            transfer, obj_created = ZoteroTransfer.objects.update_or_create(
                                publication=publication,
                                api_key=api_key,
                                path=path,
                                key=zotero_key,
                                defaults=dict(
                                    attachment_key=attachments.get(zotero_key),
                                    collection_keys=collection_keys,
                                    version=version,
                                    created=date_added,
                                    updated=date_modified,
                                    last_transferred=now,
                                )
                            )
                        except IntegrityError as err:
                            self.stderr.write(
                                f'API_KEY: {api_key}, PATH: {path}. '
                                f'Zotero Transfer couldn\'t be created. Error: {err}'
                            )
                            continue
                        except Publication.DoesNotExist:
                            continue

                        if obj_created:
                            created += 1
                        else:
                            updated += 1

            self.stdout.write(f'{created} transfers have been created')
            self.stdout.write(f'{updated} transfers have been updated')

    def get_attachments(self, api_key: str, path: str) -> dict:
        attachments = {}

        url = f'{build_zotero_api_url(path)}?itemType=attachment&limit={MAX_ITEMS_PER_REQUEST}'
        headers = get_zotero_api_headers(api_key)

        session = TimeOutSession(settings.ZOTERO_API_TIMEOUT)

        while url:
            response = session.request('GET', url, headers=headers)

            next = response.links.get('next')
            url = next and next.get('url')

            for item in response.json():
                attachment_key = item.get('key')
                data = item.get('data')
                publication_key = data.get('parentItem')

                attachments[publication_key] = attachment_key

        return attachments
