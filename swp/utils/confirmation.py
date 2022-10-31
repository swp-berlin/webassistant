YES_NO = {
    'y': True,
    'Y': True,
    'yes': True,
    'YES': True,
    'n': False,
    'N': False,
    'no': False,
    'NO': False,
}

TRUE_FALSE = {
    **YES_NO,
    1: True,
    '1': True,
    True: True,
    'TRUE': True,
    'True': True,
    'true': True,
    't': True,
    0: False,
    '0': False,
    False: False,
    'FALSE': False,
    'False': False,
    'false': False,
    'f': False,
    None: False,
}


def ask(question, default=False, truthy=None):
    response = input(question).strip()

    return (truthy or YES_NO).get(response, default)


confirm = ask

