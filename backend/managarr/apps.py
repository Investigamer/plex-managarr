# Standard Library Imports
from pathlib import Path

# Third Party Imports
from django.apps import AppConfig

# Local Imports
from managarr import settings


class ManagarrConfig(AppConfig):

    # Django Attributes
    name: str = 'managarr'
    default_auto_field: str = 'django.db.models.BigAutoField'

    # Paths
    CWD = Path(__file__).resolve().parent

    # Environment
    ENV = settings.ENV
    PlexAPI = settings.PLEX_API
