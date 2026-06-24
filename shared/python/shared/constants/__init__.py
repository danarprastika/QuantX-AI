"""Shared constants for QuantX AI."""

EXCHANGES = ["binance", "coinbase", "kraken"]
DEFAULT_TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]
EVENT_TYPES = [
    "strategy.created",
    "strategy.updated",
    "strategy.deleted",
    "position.opened",
    "position.closed",
    "order.placed",
    "order.filled",
    "order.cancelled",
]
