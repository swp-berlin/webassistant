from django.test import TestCase

from swp.models import Category
from swp.utils.testing import create_user, login, request


class CategoryViewSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('category')
        cls.categories = Category.objects.bulk_create([
            Category(name=f'Test {index + 1}') for index in range(5)
        ])

    def setUp(self):
        login(self)

    def test_choices(self):
        response = request(self, '1:category-choices')

        self.assertEqual(len(self.categories), len(response.data))
