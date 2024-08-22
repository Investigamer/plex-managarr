# Standard Library Imports
from time import perf_counter

# Third Party Imports
import click
from omnitils.files import mkdir_full_perms
from omnitils.test import time_function

# Local Imports
from managarr import settings
from managarr.settings import LOGR
from managarr.sources import identify_and_scrape
from managarr.utils._schema import MovieCollection
from managarr.utils.export import export_movie_collection

# Paths
export_dir = settings.BASE_DIR / 'export'
mkdir_full_perms(export_dir)


"""
* Commands
"""


@click.command(help='Add a movie collection from TPDB or Mediux to Kometa metadata and collection yaml files.')
@click.argument('url')
@time_function('That took {t:2f} seconds!')
def generate_movie_collection(url: str) -> None:
    """Add a movie collection from TPDB or Mediux to Kometa metadata and collection yaml files.

    Args:
        url: URL of the collection.
    """

    # Scrape from the appropriate source
    _collection = identify_and_scrape(url)

    # Movie collection
    if not isinstance(_collection, MovieCollection):
        return LOGR.warning(f'The URL provided is not a Movie collection!')

    LOGR.info(f'Movie processed: {_collection.title}')
    export_movie_collection(
        url=url,
        path=export_dir,
        collection=_collection)


"""
* Command Groups
"""


@click.group(
    commands={
        'movies': generate_movie_collection
    }
)
def GenerateGroup():
    """Command group for generating YAML files."""
    pass
