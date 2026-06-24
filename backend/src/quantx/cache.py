"""Redis cache client initialization for QuantX AI."""

from redis.asyncio import Redis

from quantx.config import get_settings

settings = get_settings()

_redis_client: Redis | None = None


def get_redis() -> Redis:
    """Return the Redis async client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(
            str(settings.redis.url),
            decode_responses=True,
            max_connections=settings.redis.max_connections,
        )
    return _redis_client


async def close_redis() -> None:
    """Close the Redis connection."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None


async def health_check() -> bool:
    """Check Redis connectivity."""
    try:
        client = get_redis()
        await client.ping()
        return True
    except Exception:
        return False
