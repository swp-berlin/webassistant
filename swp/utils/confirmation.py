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
    True: True,
    'TRUE': True,
    'True': True,
    'true': True,
    't': True,
    False: False,
    'FALSE': False,
    'False': False,
    'false': False,
    'f': False,
    None: False,
}

ZERO_ONE = {
    1: True,
    '1': True,
    0: False,
    '0': False,
}

ON_OFF = {
    'ON': True,
    'on': True,
    'OFF': False,
    'off': False,
}

TRUTHY = {
    **YES_NO,
    **TRUE_FALSE,
    **ZERO_ONE,
    **ON_OFF,
}


def ask(question, default=False, truthy=None):
    response = input(question).strip()

    return (truthy or YES_NO).get(response, default)


confirm = ask
