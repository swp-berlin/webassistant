from tldextract import TLDExtract

EXTRA_TOP_LEVEL_DOMAINS = [
    'ox.ac.uk',
    'europa.eu',
    'house.gov',
    'senate.gov',
]

extract = TLDExtract(extra_suffixes=EXTRA_TOP_LEVEL_DOMAINS)


def get_canonical_domain(url: str) -> str:
    return extract(url).registered_domain


def is_subdomain(url: str, domain: str) -> bool:
    return get_canonical_domain(url) == domain
