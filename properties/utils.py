import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def get_redis_cache_metrics():
    """
    Retrieves Redis cache metrics (keyspace hits, misses, and hit ratio).

    Returns:
        dict: {
            'keyspace_hits': int,
            'keyspace_misses': int,
            'hit_ratio': float
        }
    """
    try:
        # Get Redis connection from Django cache backend
        redis_conn = get_redis_connection("default")

        # Fetch Redis INFO stats
        info = redis_conn.info()

        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)

        total = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total) if total > 0 else 0

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