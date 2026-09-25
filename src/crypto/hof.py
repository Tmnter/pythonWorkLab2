import operator
from typing import Any, Callable


def pipe(*funcs: Callable) -> Callable:
    def inner(value: Any) -> Any:
        res = value
        for f in funcs:
            res = f(res)
        return res

    return inner


def compose(*funcs: Callable) -> Callable:
    return pipe(*reversed(funcs))


# Оновлена функція з вашого скріншота
def make_predicate(field: str, op_name: str, value: Any) -> Callable[[dict], bool]:
    # Отримуємо бінарну операцію з модуля operator ("ge", "eq", "lt" тощо)
    op_func = getattr(operator, op_name)
    return lambda rec: op_func(rec[field], value)


def make_running_total() -> Callable[[float], float]:
    total = 0.0

    def accumulator(amount: float) -> float:
        nonlocal total
        total += amount
        return total

    return accumulator


def scale(factor: float, value: float) -> float:
    return round(factor * value, 2)


def curry3(f: Callable) -> Callable:
    return lambda a: lambda b: lambda c: f(a, b, c)