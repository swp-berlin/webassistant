from typing import Iterable


ISBN_DIGITS = '0123456789X'
LEGAL_DIGITS = '0123456789Xx'


def isbn_digits(value: str) -> Iterable[str]:
    return (v.upper() for v in value if v in LEGAL_DIGITS)


def count_isbn_digits(value: str) -> int:
    return sum(1 for v in value if v in LEGAL_DIGITS)


def canonical_isbn(value: str) -> str:
    s = str.strip(value or '')
    if not s:
        return ''

    digits = isbn_digits(s)
    return ''.join(digits)


def normalize_isbn(value: str) -> str:
    s = str.strip(value or '')
    if not s:
        return ''

    return s.upper()
