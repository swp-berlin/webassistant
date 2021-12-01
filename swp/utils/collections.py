from typing import Iterator, List


def chunked(lst: list, n: int) -> Iterator[List[dict]]:
    if n < 1:
        raise ValueError('chunk size must be greater than 0')

    for i in range(0, len(lst), n):
        yield lst[i: i + n]
