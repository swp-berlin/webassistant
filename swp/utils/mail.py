from functools import partial

from django.core.mail import send_mail as django_send_mail
from django.template.loader import render_to_string

EXTENSIONS = (
    'subject',
    'plain',
    'html',
)


def send_mail(identifier, *recipients, request=None, options=None, context):
    subject, plain, html = render_mail(identifier, request=request, context=context)

    defaults = {
        'from_email': None,
        'subject': subject,
        'message': plain,
        'html_message': html,
        'recipient_list': [*recipients],
    }

    if options:
        defaults.update(options)

    return django_send_mail(**defaults)


def render_mail(identifier, *, request=None, context):
    render = partial(render_to_string, context=context, request=request)
    subject, plain, html = [render(f'mails/{identifier}.{extension}') for extension in EXTENSIONS]

    return clean_subject(subject), plain, html


def clean_subject(subject):
    """
    Subject should not contain any newlines.
    """

    subject = str.strip(subject)
    words = str.split(subject)

    return ' '.join(words)
