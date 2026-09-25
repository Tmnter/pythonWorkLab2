from dataclasses import dataclass, replace
from typing import Any


@dataclass(frozen=True)
class Record:
    asset: str
    amount: float
    price: float


def create_record(data: dict[str, Any]) -> Record:
    return Record(
        asset=str(data["asset"]),
        amount=float(data["amount"]),
        price=float(data["price"]),
    )


def update_record(rec: Record, **changes: Any) -> Record:
    return replace(rec, **changes)