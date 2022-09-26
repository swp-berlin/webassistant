import os

from contextlib import contextmanager

from .filepath import FilePath


@contextmanager
def working_directory(path: FilePath):
    current = os.getcwd()

    try:
        yield os.chdir(path)
    finally:
        os.chdir(current)


cd = working_directory


def ensure_directory(filepath: FilePath):
    directory = os.path.dirname(filepath)

    os.makedirs(directory, exist_ok=True)

    return directory
