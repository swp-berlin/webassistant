from functools import partial
from typing import Iterable, Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def get_user_queryset(is_active: bool = None, **filter_kwargs) -> QuerySet:
    if is_active is not None:
        filter_kwargs['is_active'] = is_active

    return get_user_model().objects.filter(**filter_kwargs)


def get_user_email_addresses(is_active: Optional[bool] = True, **filter_kwargs) -> Iterable[str]:
    queryset = get_user_queryset(is_active=is_active, **filter_kwargs)
    email_field = queryset.model.get_email_field_name()

    queryset = queryset.exclude(
        **{email_field: ''}
    ).distinct(email_field).order_by(email_field)

    return queryset.values_list(email_field, flat=True)


get_superuser_email_addresses = partial(get_user_email_addresses, is_superuser=True)
