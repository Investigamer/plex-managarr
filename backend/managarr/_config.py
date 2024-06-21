"""
* Project Configuration
"""
# Standard Library Import
from pathlib import Path

# Third Party Imports
from omnitils.files import load_data_file


class AppEnvironment:

    # Paths
    CWD = Path(__file__).parent.parent
    PATH_ENV = CWD / 'env.yml'

    def __init__(self):
        try:
            self._env = load_data_file(self.PATH_ENV)
        except (FileNotFoundError, ValueError, OSError):
            self._env = {}
        self.TMDB_TOKEN = self._env.get('TMDB_TOKEN', '')


# Create app objects
ENV = AppEnvironment()
__all__ = ['ENV']
