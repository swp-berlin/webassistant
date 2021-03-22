from argparse import ArgumentParser

from django.core.management import BaseCommand

from swp.tasks import run_scraper


class Command(BaseCommand):

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('pk', type=int)

    def handle(self, pk, **kwargs):
        run_scraper.delay(pk, force=True)
