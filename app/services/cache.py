import time
from typing import Any, Optional

_CACHE: dict[str, tuple[float, Any]] = {}
TTL_SECONDS = 300

def get(key: str) -> Optional[Any]:
    item = _CACHE.get(key)
    if not item:
        return None
    
    expires_at, value = item
    if time.time() > expires_at:
        _CACHE.pop(key, None)
        return None
    
    return value

def set (key: str, value: Any):
    expires_at = time.time() + TTL_SECONDS
    _CACHE[key] = (expires_at, value)