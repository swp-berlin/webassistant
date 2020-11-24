from django.template import Library

from swp.utils.version import get_version

register = Library()

register.simple_tag(name='version')(get_version)
