from django.conf import settings as django_settings


def settings(request):
    return {
        'ENVIRONMENT': django_settings.ENVIRONMENT,
        'RELEASE': django_settings.RELEASE,
    }
