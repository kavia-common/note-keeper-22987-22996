"""
OpenAPI tag constants for the Ocean Professional Notes API.
This centralizes tag naming to keep documentation consistent.
"""
# PUBLIC_INTERFACE
def get_openapi_tags():
    """Return default OpenAPI tags list for drf_yasg configuration."""
    return [
        {"name": "notes", "description": "Operations related to notes"},
        {"name": "health", "description": "Service health endpoints"},
    ]
