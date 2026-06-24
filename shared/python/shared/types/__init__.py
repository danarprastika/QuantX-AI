"""Shared type definitions for QuantX AI."""

from enum import Enum

from decimal import Decimal


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


Symbol = str
AccountId = str
