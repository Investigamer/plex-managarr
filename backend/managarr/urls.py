"""
* URL configuration for Plex Managarr API
"""
# Third Party Imports
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

# Local Imports
from managarr.routes.plex import api as route_plex

# Add our API endpoints
APIRouter = NinjaAPI(
    docs_url='docs/',
    title='Plex Managarr API')
APIRouter.add_router('/plex/', route_plex)

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', APIRouter.urls)
]
