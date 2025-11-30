import redis
import json
import os
from functools import wraps
from flask import current_app




redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    decode_responses=True
)





def cache_key(prefix, *args):
    return f"{prefix}:{':'.join(str(arg) for arg in args)}"





def cache_get(key):
        value = redis_client.get(key)
        return json.loads(value) if value else None




def cache_set(key, value, expire=300):
        redis_client.setex(key, expire, json.dumps(value))
        return True




def cache_delete(key):
        redis_client.delete(key)
        return True




def cache_clear_pattern(pattern):
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True




def cached(expire=300, key_prefix="default"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key_name = cache_key(key_prefix, func.__name__, *args, *kwargs.values())
            
            cached_result = cache_get(cache_key_name)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache_set(cache_key_name, result, expire)
            return result
        return wrapper
    return decorator