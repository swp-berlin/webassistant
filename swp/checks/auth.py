from django.core import checks
from django.core.checks import Warning

from django.contrib.auth.models import Group
from django.db import ProgrammingError


@checks.register()
def check_groups(app_configs, **kwargs):
    """ Check if all required groups are available. """
    try:
        return perform_check_gropus()
    except ProgrammingError:
        # there is an issue with the database setup
        # this might happen, if the check is run before database setup, e.g. with test settings
        # we skip this for now
        return []


def perform_check_gropus():
    errors = []

    for group_name in [
        'swp-useradmin',
        'swp-manager',
        'swp-editor',
    ]:
        try:
            Group.objects.get_by_natural_key(group_name)
        except Group.DoesNotExist:
            errors += [
                Warning(
                    f'Missing group "{group_name}" in database',
                    hint='Install groups fixture via loaddata',
                    obj=Group,
                    id='swp.W001',
                )
            ]

    return errors
