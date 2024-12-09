import time

from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class Timer:
    start: float
    end: float = None
    duration: float = None


@contextmanager
def timed():
    start = time.perf_counter()
    timer = Timer(start)

    try:
        yield timer
    finally:
        timer.end = end = time.perf_counter()
        timer.duration = end - start


def format_duration(duration: float):
    if duration > 60:
        duration = round(duration)

    hours, minutes = divmod(duration, 60 * 60)
    minutes, seconds = divmod(minutes, 60)
    hours, minutes = int(hours), int(minutes)
    values = hours, minutes, seconds

    return ' '.join([f'{value}{char}' for value, char in zip(values, 'hms') if value])
