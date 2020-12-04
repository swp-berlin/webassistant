from django.core import checks
from django.core.checks import Warning

from django.contrib.auth.models import Group


@checks.register()
def check_groups(app_configs, **kwargs):
    """ Check if all required groups are available. """
    errors = []

    for group_name in [
        'swp-superuser',
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
                )
            ]

    return errors
