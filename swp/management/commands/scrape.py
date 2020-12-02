import asyncio
from argparse import ArgumentParser

from django.core.management import BaseCommand

from swp.models import Scraper


class Command(BaseCommand):

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('pk', type=int)

    def handle(self, pk, **kwargs):
        scraper = Scraper.objects.get(pk=pk)

        asyncio.run(scraper.scrape())
