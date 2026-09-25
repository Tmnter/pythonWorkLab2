import math
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Num:
    value: float


@dataclass(frozen=True)
class Neg:
    x: "Expr"


@dataclass(frozen=True)
class Add:
    a: "Expr"
    b: "Expr"


@dataclass(frozen=True)
class Sub:
    a: "Expr"
    b: "Expr"


@dataclass(frozen=True)
class Mul:
    a: "Expr"
    b: "Expr"


@dataclass(frozen=True)
class Div:
    a: "Expr"
    b: "Expr"


@dataclass(frozen=True)
class Pow:
    base: "Expr"
    exp: int


@dataclass(frozen=True)
class Sqrt:
    x: "Expr"


@dataclass(frozen=True)
class Sum:
    terms: tuple["Expr", ...]


Expr = Union[Num, Neg, Add, Sub, Mul, Div, Pow, Sqrt, Sum]


def evaluate(node: Expr) -> float:
    match node:
        case Num(0 | 0.0):
            return 0.0

        case Num(v):
            return float(v)

        case Sum(()):
            return 0.0

        case Sum((head, *tail)):
            return evaluate(head) + evaluate(Sum(tuple(tail)))

        case Pow(base, exp) if exp >= 0:
            return evaluate(base) ** exp

        case Pow(_, exp):
            raise ValueError(f"від'ємний показник: {exp}")

        case Neg(x):
            return -evaluate(x)

        case Add(a, b):
            return evaluate(a) + evaluate(b)

        case Sub(a, b):
            return evaluate(a) - evaluate(b)

        case Mul(a, b):
            return evaluate(a) * evaluate(b)

        case Div(a, b):
            b_val = evaluate(b)
            if b_val == 0:
                raise ValueError("ділення на нуль")
            return evaluate(a) / b_val

        case Sqrt(x):
            x_val = evaluate(x)
            if x_val < 0:
                raise ValueError(f"корінь із від'ємного числа: {x_val}")
            return math.sqrt(x_val)

        case _:
            raise ValueError(f"невідомий вузол: {node!r}")