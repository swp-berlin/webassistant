def is_subdomain(subdomain: str, domain: str) -> bool:
    subdomain = str.lower(subdomain).split('.')
    domain = str.lower(domain).split('.')

    if subdomain == domain:
        return True

    if len(domain) > len(subdomain):
        return False

    return subdomain[-len(domain):] == domain
