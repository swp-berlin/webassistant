from cosmogo.commands.gettext import UpdateTranslationsCommand


class Command(UpdateTranslationsCommand):
    APPLICATION = 'swp'
    IGNORE = [
        *UpdateTranslationsCommand.IGNORE,
        'assets/i18n',
    ]
