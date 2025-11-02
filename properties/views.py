from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from .utils import get_all_properties

@csrf_exempt
@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    Returns all property listings as JSON.
    Caches the result in Redis for performance.
    """
    properties = get_all_properties()
    data = [
        {
            "id": prop.id,
            "title": prop.title,
            "description": prop.description,
            "price": float(prop.price),
            "location": prop.location,
            "created_at": prop.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for prop in properties
    ]
    return JsonResponse({"properties": data}, safe=False)