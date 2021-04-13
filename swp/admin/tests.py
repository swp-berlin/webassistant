from django.contrib.admin import site as admin_site
from django.contrib.auth.models import Group
from django.test import TestCase
from django.utils import timezone

from cosmogo.utils.testing import login, request, admin_url

from swp.models import (
    Monitor,
    Publication,
    PublicationFilter,
    Scraper,
    ScraperError,
    Thinktank,
    ThinktankFilter,
)
from swp.models.choices import Comparator, DataResolverKey
from swp.scraper.types import ScraperType
from swp.utils.testing import create_superuser


class AdminTestCase(TestCase):

    EXCLUDE = {
        Group,
    }

    @classmethod
    def setUpModels(cls, now):
        monitor = Monitor.objects.create(name='Test-Monitor', recipients=[cls.user.email])
        thinktank = Thinktank.objects.create(
            name='Test-Thinktank',
            url='https://www.piie.com/',
            unique_fields=['T1-AB'],
        )
        thinktank_filter = ThinktankFilter.objects.create(thinktank=thinktank, monitor=monitor)
        PublicationFilter.objects.create(
            thinktank_filter=thinktank_filter,
            field=DataResolverKey.TITLE,
            comparator=Comparator.STARTS_WITH,
            values=['Taming'],
        )

        scraper = Scraper.objects.create(
            thinktank=thinktank,
            type=ScraperType.LIST_WITH_LINK_AND_DOC.value,
            data={'hue?': 'hue!'},
            start_url='https://www.piie.com/research/publications/policy-briefs',
            checksum='de9474fa85634623fd9ae9838f949a02c9365ede3499a26c9be52363a8b7f214',
        )
        ScraperError.objects.create(scraper=scraper, code='error', message="You're a test case, Harry!")

        publication = Publication.objects.create(
            thinktank=thinktank,
            title='Taming the US trade deficit: A dollar policy for balanced growth',
            url='https://www.piie.com/publications/policy-briefs/taming-us-trade-deficit-dollar-policy-balanced-growth',
        )

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.user = create_superuser()

        cls.setUpModels(now=now)
        cls.models = {*admin_site._registry} - cls.EXCLUDE

    def setUp(self):
        login(self)

    def assertModelExists(self, model):
        obj = model.objects.first()

        self.assertTrue(obj, msg=(
            'Make sure to have at least one instance of each model. '
            '%s.%s does not have any objects.' % (
                model._meta.app_label,
                model._meta.object_name,
            )
        ))

        self.assertTrue('%s' % obj)

        return obj

    def helper_for_model(self, get_url, models=None):
        for model in (models or self.models):
            with self.subTest(model=model):
                obj = self.assertModelExists(model)
                url = get_url(obj)

                request(self, url)

    def test_change_lists(self):
        def get_url(model):
            return admin_url(model, 'changelist')

        return self.helper_for_model(get_url)

    def test_add_forms(self):
        def get_url(model):
            return admin_url(model, 'add')

        return self.helper_for_model(get_url, self.models)

    def test_change_forms(self):
        def get_url(obj):
            return admin_url(obj, 'change', obj.pk)

        return self.helper_for_model(get_url)
