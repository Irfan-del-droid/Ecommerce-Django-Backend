"""
URL configuration for loki_backend project.
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
import os


def root(request):
    """GET / — API has no HTML homepage; this avoids opaque 404s in the dev server log."""
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    # Handle GET and HEAD requests
    if request.method in ['GET', 'HEAD']:
        response = JsonResponse({
            "service": "Loki Stores API",
            "api_base": "/api/",
            "admin": "/admin/",
            "hint": "Open the React app at http://localhost:3000 for the storefront UI.",
        })
        # Add CORS headers for all responses
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    # Method not allowed
    return HttpResponse(status=405)


def favicon_view(request):
    """Serve favicon.ico from static files."""
    import os
    from django.conf import settings
    from django.http import HttpResponse

    # Try staticfiles directory first (production)
    favicon_path = os.path.join(settings.STATIC_ROOT, 'favicon.ico')
    if os.path.exists(favicon_path):
        try:
            with open(favicon_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='image/x-icon')
                response['Cache-Control'] = 'public, max-age=86400'
                response['Access-Control-Allow-Origin'] = '*'
                return response
        except Exception as e:
            print(f"Error reading favicon from STATIC_ROOT: {e}")

    # Fallback: serve from source static directory
    source_path = os.path.join(settings.BASE_DIR, 'static', 'favicon.ico')
    if os.path.exists(source_path):
        try:
            with open(source_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='image/x-icon')
                response['Cache-Control'] = 'public, max-age=86400'
                response['Access-Control-Allow-Origin'] = '*'
                return response
        except Exception as e:
            print(f"Error reading favicon from static: {e}")

    # Last resort: return 404
    print(f"Favicon not found. STATIC_ROOT: {settings.STATIC_ROOT}, BASE_DIR: {settings.BASE_DIR}")
    return HttpResponse(status=404)


# Global API URL configuration
api_version = 'api/'

urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    
    # Serve favicon.ico
    path('favicon.ico', favicon_view),
    
    # App URLs with proper namespacing
    path(f'{api_version}auth/', include('accounts.urls')),
    path(f'{api_version}', include('products.urls')),
    path(f'{api_version}newsletter/', include('newsletter.urls')),
    path(f'{api_version}contact/', include('contacts.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
