from typing import Any, NamedTuple


class Result(NamedTuple):
    ok: bool
    value: Any
    error: str | None


def parse(line: str) -> dict[str, Any] | None:
    parts = line.strip().split(",")
    if len(parts) != 3:
        return None
    asset, amount_str, price_str = parts
    try:
        return {
            "asset": asset.strip(),
            "amount": float(amount_str),
            "price": float(price_str),
        }
    except ValueError:
        return None


def normalize(rec: dict[str, Any]) -> dict[str, Any]:
    return {
        "asset": str(rec["asset"]).lower(),
        "amount": float(rec["amount"]),
        "price": float(rec["price"]),
    }


def process(line: str) -> Result:
    parsed = parse(line)
    if parsed is None:
        return Result(ok=False, value=None, error="Некоректний формат рядка")
    return Result(ok=True, value=normalize(parsed), error=None)