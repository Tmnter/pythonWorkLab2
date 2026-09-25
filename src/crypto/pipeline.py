from functools import reduce
from typing import Callable, Generator, Iterable

from src.crypto.hof import make_predicate
from src.crypto.parse import normalize, parse

# Варіант 15: відбір за amount >= 5.0
keep = make_predicate("amount", "ge", 5.0)


# --- 4.1. Map / Filter / Reduce ---
def aggregate_pipeline(lines: Iterable[str]) -> dict[str, float]:
    parsed_stream = filter(None, map(parse, lines))
    normalized_stream = map(normalize, parsed_stream)
    filtered_stream = filter(keep, normalized_stream)

    def add_to_groups(acc: dict[str, float], rec: dict) -> dict[str, float]:
        acc[rec["asset"]] = acc.get(rec["asset"], 0.0) + rec["amount"]
        return acc

    return reduce(add_to_groups, filtered_stream, {})


# --- 4.2. List Comprehensions ---
def aggregate_comprehension(lines: Iterable[str]) -> dict[str, float]:
    parsed = [p for line in lines if (p := parse(line)) is not None]
    normalized = [normalize(rec) for rec in parsed]
    filtered = [rec for rec in normalized if keep(rec)]

    acc: dict[str, float] = {}
    for rec in filtered:
        acc[rec["asset"]] = acc.get(rec["asset"], 0.0) + rec["amount"]

    return acc


# --- 6. Генератори ---
def read_lines(filepath: str) -> Generator[str, None, None]:
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            yield line


def lazy_filter(
    predicate: Callable[[dict], bool], iterable: Iterable[dict]
) -> Generator[dict, None, None]:
    for item in iterable:
        if predicate(item):
            yield item


def lazy_running_total(iterable: Iterable[dict]) -> Generator[float, None, None]:
    total = 0.0
    for rec in iterable:
        total += rec["amount"]
        yield total