"""
* Collect Data from ThePosterDB.com
"""
# Standard Library Imports
from contextlib import suppress
from typing import Optional

import yarl
# Third Party Imports
from bs4 import BeautifulSoup, Tag
from omnitils.logs import logger
from omnitils.schema import Schema

# Local Imports
from managarr.utils._schema import Movie, MovieCollection, TVShow, TVSeason, TVEpisode, MediaSources, MediaTypes
from managarr.sources.themoviedb import get_movie_id

"""
* Schemas
"""


class BasePoster(Schema):
    """Represents a poster with only basic attributes."""
    media_type: MediaTypes
    title: str
    url_poster: Optional[str] = None
    url_background: Optional[str] = None
    source: MediaSources
    id_tmdb: Optional[int] = None


"""
* Build Schema Objects
"""


def get_tv_show(tmdb_token: str, show: BasePoster, seasons: list[TVSeason] = None) -> TVShow:
    """Format tv show data."""
    if seasons is None:
        seasons = []

    # Get title and year
    title = show.title.split(" (")[0]
    try:
        year = int(title.split(" (")[1].split(")")[0])
    except IndexError:
        year = None

    # Return data
    return TVShow(
        title=title,
        url_poster=show.url_poster,
        seasons=seasons,
        year=year,
        source=show.source,
        id_tmdb=get_movie_id(tmdb_token, title) if show.id_tmdb is None else show.id_tmdb
    )


def get_tv_season(season: BasePoster, episodes: list[TVEpisode] = None) -> TVSeason:
    """Format tv season data."""
    if episodes is None:
        episodes = []

    # Format title and season number
    split_season = season.title.split(" - ")[1].strip()
    number = 0 if split_season == "Specials" else int(split_season.split(" ")[1])

    # Return data
    return TVSeason(
        number=number,
        url_poster=season.url_poster,
        episodes=episodes,
        source=season.source
    )


def get_tv_episode(episode: BasePoster) -> TVEpisode:
    """Format tv episode data."""
    # Todo: Not yet implemented on ThePosterDB
    return TVEpisode(
        number=1,
        url_title_card=episode.url_poster,
        source=episode.source
    )


def get_movie(tmdb_token: str, movie: BasePoster) -> Movie:
    """Format movie data."""

    # Get title and year
    title_split = movie.title.split(" (")
    title = f'{title_split[0]} ({title_split[1]}' if len(title_split[1]) != 5 else title_split[0]
    try:
        year = int(title_split[-1].split(")")[0])
    except IndexError:
        year = None

    # Return data
    return Movie(
        title=title,
        url_poster=movie.url_poster,
        year=year,
        id_tmdb=get_movie_id(tmdb_token, title, year),
        source=movie.source)


def get_movie_collection(collection: BasePoster, movies: list[Movie] = None) -> MovieCollection:
    """Format movie collection data."""
    if movies is None:
        movies = []

    # Return data
    return MovieCollection(
        title=collection.title,
        url_poster=collection.url_poster,
        movies=movies,
        source=collection.source
    )


"""
* Page Classes
"""


class PosterDBPage:
    media_map: dict[str, MediaTypes] = {
        'Movie': MediaTypes.Movie,
        'Collection': MediaTypes.MovieCollection,
        'Show': MediaTypes.TVShow,
    }

    def __init__(self, tmdb_token: str, soup: BeautifulSoup):
        self.soup = soup
        self.tmdb_token = tmdb_token
        self.main_set: Optional[BasePoster] = None
        self.posters = self.get_posters()

    def get_poster_tags(self) -> list[Tag]:
        """Returns a list of HTML tags containing poster data, extracted from the main tag."""
        main_tag = self.soup.find('div', class_='row d-flex flex-wrap m-0 w-100 mx-n1 mt-n1')
        return main_tag.find_all('div', class_='col-6 col-lg-2 p-1')

    def get_posters(self) -> list[BasePoster]:
        """Returns a list of BasePoster objects with attributes provided by its poster tag."""
        posters = []
        for n in self.get_poster_tags():

            # Extract the media type
            media_type = n.find(
                'a', class_="text-white",
                attrs={
                    'data-toggle': 'tooltip',
                    'data-placement': 'top'
                })['title']
            media_type = self.media_map.get(media_type)
            if media_type is None:
                continue

            # Extract the title and URL ID
            title = n.find('p', class_='p-0 mb-1 text-break').string
            url_id = n.find('div', class_='overlay').get('data-poster-id')

            # Delineate between show and season
            checks = [') - Season', ') - Specials']
            if media_type == MediaTypes.TVShow and any(n in title for n in checks):
                media_type = MediaTypes.TVSeason

            # Add this poster
            obj = BasePoster(
                    media_type=media_type,
                    title=title,
                    url_poster=f'https://theposterdb.com/api/assets/{url_id}',
                    source=MediaSources.PosterDB)
            if media_type in [MediaTypes.TVShow, MediaTypes.MovieCollection]:
                # Separate main collection/show poster
                self.main_set = obj
                continue
            posters.append(obj)

        return posters

    def get_movies(self) -> list[Movie]:
        """Returns a list of Movie objects formatted from BasePoster objects."""
        movie_list: list[Movie] = [
            get_movie(self.tmdb_token, n) for n in self.posters
            if n.media_type == MediaTypes.Movie]
        with suppress(KeyError, TypeError, ValueError):
            movie_list = sorted(movie_list, key=lambda x: x.year)
        return movie_list

    def get_seasons(self) -> list[TVSeason]:
        """Returns a list of TVSeason objects formatted from BasePoster objects."""
        season_list = [get_tv_season(n) for n in self.posters if n.media_type == MediaTypes.TVSeason]
        with suppress(KeyError, TypeError, ValueError):
            season_list = sorted(season_list, key=lambda x: x.number)
        return season_list

    def get_collection(self) -> Optional[MovieCollection | TVShow]:
        """Check whether this is a Movie collection or a TV Show, then build and return the appropriate object."""
        if self.main_set is not None:
            if self.main_set.media_type == MediaTypes.TVShow:
                return get_tv_show(self.tmdb_token, self.main_set, self.get_seasons())
            if self.main_set.media_type == MediaTypes.MovieCollection:
                return get_movie_collection(self.main_set, self.get_movies())
        return logger.error('No main collection or show poster was found on this page!')


"""
* Utilities
"""


def get_set_from_poster(soup) -> Optional[yarl.URL]:
    """Extract collection URL from page.

    Args:
        soup: BeautifulSoup object to extract collection URL from.

    Returns:
        Collection URL.
    """
    with suppress(Exception):
        url = soup.find('a', class_='rounded view_all')['href']
        return yarl.URL(url)
    return None
