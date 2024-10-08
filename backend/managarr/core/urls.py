"""
* URL configuration for Plex Managarr API
"""
# Third Party Imports
from django.contrib import admin
from django.urls import path

# Local Imports
from managarr.api.urls import APIRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', APIRouter.urls)
]
