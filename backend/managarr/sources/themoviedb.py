"""
* Collect Data from TMDB API
"""
# Standard Library Imports
from contextlib import suppress
from json import JSONDecodeError
from typing import Optional, Callable

# Third Party Imports
import requests
import yarl
from omnitils.fetch import request_header_default
from omnitils.logs import logger

"""
* TMDB API
"""


def get_search(
    token: str,
    url: yarl.URL | str,
    query: dict,
    sort_with: Callable = lambda k: k['release_date'][:4],
    sort_reverse: bool = False,
    header: Optional[dict] = None
) -> list[dict]:
    """Return a list from an TMDB API search query."""

    # Format the request headers
    header = header or request_header_default.copy()
    header.update({
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    })

    # Request the data
    with requests.get(url, headers=header) as r:
        r.raise_for_status()

        # Parse the results
        try:
            results = r.json()['results']
        except (JSONDecodeError, KeyError):
            logger.error('Failed to parse JSON response!')
            return []

        # Check for no results returned
        if not results:
            logger.warning(f'No results were found matching provided query:\n{query}')
            return []

        # Sort and return the results
        if sort_with is not None:
            with suppress(Exception):
                sorted_results = sorted(results, key=sort_with, reverse=sort_reverse)
                return sorted_results
            # Sorting failed
            logger.warning('Couldn\'t sort results using the provided expression! Returning unsorted results.')
            return results
        return results


def get_search_movie(
        query: dict,
        token: str,
        sort_with: Callable = lambda k: k['release_date'][:4],
        sort_reverse: bool = False,
        header: Optional[dict] = None
) -> list[dict]:
    """Return a list of movies matching a provided name from an TMDB API search query."""

    # Define the query URL
    url = yarl.URL("https://api.themoviedb.org/3/search/movie").with_query(query)
    return get_search(
        token=token,
        url=url,
        query=query,
        sort_with=sort_with,
        sort_reverse=sort_reverse,
        header=header)


def get_movie_id(token: str, name: str, year: Optional[str | int] = None) -> int:
    """Get the TMDB ID of a given movie."""

    # Define the query
    query = {'query': name}
    if year is not None:
        query['primary_release_year'] = str(year)

    # Request movie results
    items: list[dict] = get_search_movie(
        query=query,
        token=token,
        sort_with=lambda k: k['popularity'],
        sort_reverse=True)

    # Check for an empty return
    if not items:
        return logger.error('No matching movie was returned by TMDB!')
    return int(items[0]['id'])
