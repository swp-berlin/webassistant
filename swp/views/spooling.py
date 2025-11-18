import datetime

from collections import defaultdict
from pathlib import Path
from typing import List

from django.contrib.admin.sites import AdminSite
from django.http import Http404, FileResponse
from django.shortcuts import resolve_url
from django.views.generic import TemplateView

from swp.models import Publication
from swp.utils.admin import admin_url
from swp.utils.spooling import iter_files, State, get_date

SPOOLING_STATES: List[State] = [
    'error',
    'todo',
    'lost',
    'done',
]


class SpoolingView(TemplateView):
    template_name = 'admin/spooling.html'

    site: AdminSite = None
    directory: Path = None

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Spooling'
        kwargs['files'] = {state: self.get_state_info(state) for state in SPOOLING_STATES}

        return TemplateView.get_context_data(self, **kwargs)

    def get_state_info(self, state: State):
        dates = defaultdict(list)

        for publication_id, filepath in iter_files(self.directory, state):
            filename = filepath.name
            date = filepath.parent.name

            publication_url = admin_url(Publication, 'change', publication_id, site=self.site)
            download_url = resolve_url('admin:spooling', state=state, date=date, filename=filename)

            info = publication_url, download_url, filename

            dates[date].append(info)

        return dict(dates)

    @staticmethod
    def file_response(directory: Path, state: State, date: datetime.date, filename: str):
        filepath = directory / state / get_date(date) / filename

        try:
            fp = open(filepath, 'rb')
        except FileNotFoundError as error:
            raise Http404 from error

        return FileResponse(fp, filename=filename)
