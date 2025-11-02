from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Fetch all properties, using Redis cache to speed up repeated queries.
    """
    all_properties = cache.get('all_properties')

    if all_properties is None:
        logger.info("Cache miss: fetching properties from database.")
        all_properties = list(Property.objects.all().values())
        cache.set('all_properties', all_properties, 3600)  # cache for 1 hour
    else:
        logger.info("Cache hit: returning cached properties.")

    return all_properties


def get_redis_cache_metrics():
    """
    Retrieves Redis cache metrics (keyspace hits, misses, and hit ratio).
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) if total_requests > 0 else 0

        metrics = {
            "keyspace_hits": keyspace_hits,
            "keyspace_misses": keyspace_misses,
            "hit_ratio": round(hit_ratio, 3),
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": 0.0,
        }