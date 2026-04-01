"""
URL configuration for loki_backend project.
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def root(_request):
    """GET / — API has no HTML homepage; this avoids opaque 404s in the dev server log."""
    return JsonResponse({
        "service": "Loki Stores API",
        "api_base": "/api/",
        "admin": "/admin/",
        "hint": "Open the React app at http://localhost:3000 for the storefront UI.",
    })


# Global API URL configuration
api_version = 'api/'

urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    
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
