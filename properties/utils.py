from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get data from Redis
    all_properties = cache.get('all_properties')

    if all_properties is None:
        print("Cache miss: fetching from database")
        # Fetch from DB
        all_properties = list(Property.objects.all())
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', all_properties, timeout=3600)
    else:
        print("Cache hit: returning from Redis")

    return all_properties