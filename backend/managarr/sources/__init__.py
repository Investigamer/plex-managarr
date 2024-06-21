"""
* Scraping Sources
"""
# Local Imports
from typing import Optional

# Third Party Imports
from omnitils.logs import logger
import yarl

# Local Imports
import managarr.sources.mediux as Mediux
import managarr.sources.themoviedb as MovieDB
import managarr.sources.theposterdb as PosterDB
from managarr._schema import MovieCollection, TVShow
from managarr.utils.scrape import get_page_soup


def scrape_theposterdb(url: str | yarl.URL) -> Optional[MovieCollection | TVShow]:
    """Scrapes one or more collections from a target PosterDB page."""

    # Reroute poster page to parent collection
    if 'poster' in url.parts:
        url = PosterDB.get_set_from_poster(
            soup=get_page_soup(url))

    # Scrape a user page
    if 'user' in url.parts:
        return logger.error('User scraping is not currently implemented for ThePosterDB!')

    # Scrape a collection page
    if 'set' in url.parts:
        soup = get_page_soup(url)
        return PosterDB.PosterDBPage(soup).get_collection()

    # Unrecognized ThePosterDB url
    return logger.error('Unrecognized ThePosterDB URL provided!')


def scrape_mediux(url: str | yarl.URL) -> Optional[MovieCollection | TVShow]:
    """Scrapes one or more collections from a target Mediux page."""

    # Recognized page?
    if 'sets' in url.parts:
        soup = get_page_soup(url, ignore_status_code=True)
        return Mediux.MediuxPage(soup).get_collection()

    # Unrecognized Mediux url
    return logger.error('Unrecognized Mediux URL provided!')


def identify_and_scrape(url: str | yarl.URL) -> Optional[MovieCollection | TVShow]:
    """Identify data source appropriate for the URL provided, then scrape data from it."""
    if isinstance(url, str):
        url = yarl.URL(url)

    # ThePosterDB
    if 'theposterdb.com' in url.host:
        return scrape_theposterdb(url)

    # Mediux
    elif 'mediux.pro' in url.host:
        return scrape_mediux(url)

    # Return empty
    return logger.error("URL provided doesn't match a recognized source!")


# Export namespace
__all__ = ['Mediux', 'MovieDB', 'PosterDB', 'identify_and_scrape']
