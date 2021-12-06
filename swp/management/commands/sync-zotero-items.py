import re
from argparse import ArgumentParser
from itertools import chain

from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
from django.utils import timezone

from cosmogo.utils.requests import TimeOutSession

from swp.models import Monitor, ZoteroTransfer
from swp.utils.zotero import build_zotero_api_url, get_zotero_api_headers, OBJECT_KEY_ALPHABET


PUB_ID_BASE33 = re.compile('^(?P<base_33>.*)(S|SW|SWP|SWPZ|SWPZT|SWPZTA|SWPZTAP|SWPZTAPI)$')

# see https://www.zotero.org/support/dev/web_api/v3/basics#total_results
MAX_ITEMS_PER_REQUEST = 100


def get_publication_id(key: str):
    id_base_33 = PUB_ID_BASE33.match(key).group('base_33')
    length = len(id_base_33)

    pub_id = 0

    for idx, val in enumerate(id_base_33):
        pub_id += OBJECT_KEY_ALPHABET.index(val) * 33**(length - idx - 1)

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

                while url:
                    response = session.request('GET', url, headers=headers)

                    next = response.links.get('next')
                    url = next and next.get('url')

                    for item in response.json():
                        zotero_key = item.get('key')
                        publication_id = get_publication_id(zotero_key)

                        data = item.get('data')

                        collection_keys = data.get('collections')
                        version = data.get('version')
                        date_added = data.get('dateAdded')
                        date_modified = data.get('dateModified')

                        transfer, obj_created = ZoteroTransfer.objects.update_or_create(
                            publication_id=publication_id,
                            api_key=api_key,
                            path=path,
                            defaults=dict(
                                collection_keys=collection_keys,
                                version=version,
                                created=date_added,
                                updated=date_modified,
                                last_transferred=now,
                            )
                        )

                        if obj_created:
                            created += 1
                        else:
                            updated += 1

            self.stdout.write(f'{created} transfers have been created')
            self.stdout.write(f'{updated} transfers have been updated')
