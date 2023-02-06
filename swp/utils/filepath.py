import datetime
import os

from pathlib import PurePath
from typing import Optional, Union

from django.utils import timezone

FilePath = Union[PurePath, str]
Delta = Union[int, datetime.timedelta]


def last_modified(filepath: FilePath) -> Optional[datetime.datetime]:
    """
    Returns the last modified of the given filepath converted to an aware datetime.
    """

    try:
        timestamp = os.path.getmtime(filepath)
    except FileNotFoundError:
        return None

    naive = datetime.datetime.utcfromtimestamp(timestamp)

    return timezone.make_aware(naive, timezone=timezone.utc)


def is_outdated(filepath: FilePath, delta: Delta) -> bool:
    """
    Returns whether the file at the given path has been modified since
    the given delta. Returns true when the file does not exist.
    """

    timestamp = last_modified(filepath)

    if timestamp is None:
        return True

    if isinstance(delta, int):
        delta = datetime.timedelta(seconds=delta)

    now = timezone.localtime(timezone=timezone.utc)

    return timestamp < now - delta
