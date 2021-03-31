from django import test

from swp.utils.isbn import canonical_isbn


class ISBNTestCase(test.TestCase):

    def test_canonical_isbn(self):
        isbn_data = [
            ('0-340-01381-8', '0340013818'),
            ('ISBN: 9780881327373', '9780881327373'),
        ]

        for value, expected in isbn_data:
            with self.subTest():
                self.assertEqual(canonical_isbn(value), expected)

