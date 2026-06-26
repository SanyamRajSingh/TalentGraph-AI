from typing import Iterable


def clamp_score(value: float | int) -> int:
    return max(0, min(100, int(round(value))))


def overlap(left: Iterable[str], right: Iterable[str]) -> set[str]:
    right_by_key = {item.casefold(): item for item in right}
    return {
        right_by_key[item.casefold()]
        for item in left
        if item.casefold() in right_by_key
    }


def percent(part: int, total: int, default: int = 100) -> int:
    if total <= 0:
        return default
    return clamp_score(part * 100 / total)


def average(values: Iterable[int]) -> int:
    values = list(values)
    if not values:
        return 0
    return clamp_score(sum(values) / len(values))
