import fnmatch

import json

import time

from fastapi.encoders import jsonable_encoder

from app.core.config import (
    CACHE_DEFAULT_TTL_SECONDS,
    REDIS_URL
)


try:

    from redis import Redis

    from redis.exceptions import RedisError

except ImportError:

    Redis = None

    class RedisError(Exception):

        pass


memory_cache = {}


def get_redis_client():

    if Redis is None:

        return None

    try:

        client = Redis.from_url(
            REDIS_URL,
            decode_responses=True
        )

        client.ping()

        return client

    except RedisError:

        return None


def cache_get(
    key: str
):

    redis_client = get_redis_client()

    if redis_client:

        value = redis_client.get(key)

        if value is None:

            return None

        return json.loads(value)

    cached = memory_cache.get(key)

    if not cached:

        return None

    expires_at, value = cached

    if expires_at < time.time():

        memory_cache.pop(
            key,
            None
        )

        return None

    return value


def cache_set(
    key: str,
    value,
    ttl_seconds: int = CACHE_DEFAULT_TTL_SECONDS
):

    redis_client = get_redis_client()

    payload = jsonable_encoder(
        value
    )

    if redis_client:

        redis_client.setex(
            key,
            ttl_seconds,
            json.dumps(payload)
        )

        return

    memory_cache[key] = (
        time.time() + ttl_seconds,
        payload
    )


def cache_delete_pattern(
    pattern: str
):

    redis_client = get_redis_client()

    if redis_client:

        keys = list(
            redis_client.scan_iter(
                match=pattern
            )
        )

        if keys:

            redis_client.delete(
                *keys
            )

        return

    for key in list(memory_cache.keys()):

        if fnmatch.fnmatch(
            key,
            pattern
        ):

            memory_cache.pop(
                key,
                None
            )


def invalidate_dashboard_cache():

    cache_delete_pattern(
        "dashboard:*"
    )
