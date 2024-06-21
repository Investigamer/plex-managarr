# Standard Library Imports
from pathlib import Path
from time import perf_counter

from omnitils.files import mkdir_full_perms
from omnitils.logs import logger

# Local Imports
from managarr._config import ENV
from managarr._schema import MovieCollection, TVShow, TVEpisode
from managarr.sources import identify_and_scrape

"""
* Scrape The Poster DB
"""


def export_movie_collection(
    path: Path,
    collection: MovieCollection,
    short_name: bool = True
):
    """Export YAML for a Movie collection."""
    _ = '  '
    path_metadata = path / 'movies.metadata.yml'
    path_collections = path / 'movies.collections.yml'

    # Format collection title
    title = collection.title
    if short_name:
        title = title.replace(' Collection', '')
    title = title.strip()

    # Collection URLs
    url_poster = f'{_}{_}url_poster: {collection.url_poster}\n' if collection.url_poster else ''
    url_background = f'{_}{_}url_poster: {collection.url_background}\n' if collection.url_background else ''

    # Format collection metadata
    header = f'{_}# {title} | {url}'
    metadata = (f'{_}{title}:\n'
                f'{url_poster}'
                f'{url_background}'
                f'{_}{_}tmdb_movie:')

    # Format list of movies
    movie_list = [
        f'{_}{_}{_}- {n.id_tmdb:<9}# {n.title} ({n.year})'
        for n in collection.movies]

    # Join the collections output and export it
    collection_output = '\n'.join(['', header, metadata, *movie_list, ''])
    with open(path_collections, encoding='utf-8', mode='a') as f:
        f.write(collection_output)

    # Format movie metadata definitions
    movies_display = []
    for n in collection.movies:
        n_poster = f"\n{_}{_}url_poster: {n.url_poster}" if n.url_poster else ''
        n_background = f"\n{_}{_}url_background: {n.url_background}" if n.url_background else ''
        movies_display.append(
            f"{_}{n.id_tmdb}:  # {n.title} ({n.year})"
            f"{n_poster}"
            f"{n_background}"
        )

    # Join the metadata output and export it
    metadata_output = '\n'.join(['', header, *movies_display, ''])
    with open(path_metadata, encoding='utf-8', mode='a') as f:
        f.write(metadata_output)


def export_tv_show(
    path: Path,
    show: TVShow
):
    """Export YAML for a TV Show."""
    _ = '  '
    path_metadata = path / 'tv.metadata.yml'

    # Format show title
    title = show.title.strip()

    # Format show poster and background
    show_poster = f'{_}{_}url_poster: {show.url_poster}\n' if show.url_poster else ''
    show_background = f'{_}{_}url_background: {show.url_background}\n' if show.url_background else ''

    # Format collection metadata
    metadata = (f'{_}# {title} | {url}\n'
                f'{_}{show.id_tmdb}:\n'
                f'{show_poster}'
                f'{show_background}'
                f'{_}{_}seasons:')

    def _get_episode_output(_eps: list[TVEpisode]):
        """Return a formatted string of episode metadata."""
        if not _eps:
            return ''
        eps_list = [
            (f'{_}{_}{_}{_}{_}{ep.number}:\n'
             f'{_}{_}{_}{_}{_}{_}url_poster: {ep.url_title_card}')
            for ep in _eps]
        return '\n'.join(['', f'{_}{_}{_}{_}episodes:', *eps_list])

    # Format list of movies
    season_list = [
        (f'{_}{_}{_}{n.number}:\n'
         f'{_}{_}{_}{_}url_poster: {n.url_poster}'
         f'{_get_episode_output(n.episodes)}')
        for n in show.seasons]

    # Join the collections output and export it
    output = '\n'.join(['', metadata, *season_list, ''])
    with open(path_metadata, encoding='utf-8', mode='a') as f:
        f.write(output)


"""
* Launcher
"""

if __name__ == "__main__":

    # Export directory
    export_dir = ENV.CWD / 'export'
    mkdir_full_perms(export_dir)

    # Scrape The Poster DB
    while True:

        # Prompt the user for a URL
        logger.success('Please provide a collection URL ...')
        url = input()
        logger.info('Processing your request ...')
        start = perf_counter()

        # Scrape from the appropriate source
        _collection = identify_and_scrape(url)

        # Movie collection
        if isinstance(_collection, MovieCollection):
            logger.info(f'Show processed: {_collection.title}')
            export_movie_collection(
                path=export_dir,
                collection=_collection)

        # TV Show
        if isinstance(_collection, TVShow):
            logger.info(f'Movie collection processed: {_collection.title}')
            export_tv_show(
                path=export_dir,
                show=_collection)

        # Onto the next one
        elapsed = perf_counter() - start
        logger.info(f'That took {elapsed:2f} seconds!')
