"""
* Collect Data from Mediux.pro
"""
# Standard Library Imports
from typing import Optional, Union

# Third Party Imports
from bs4 import BeautifulSoup
from omnitils.logs import logger
from omnitils.properties import default_prop

# Local Imports
from managarr.utils.scrape import parse_json_string
from managarr.utils._schema import Movie, MovieCollection, TVShow, TVSeason, TVEpisode, MediaTypes, MediaSources

"""
* Types
"""

CollectionType = Union[MediaTypes.MovieCollection, MediaTypes.TVShow, None]

"""
* Classes
"""


class MediuxPage:
    url_formula = "https://api.mediux.pro/assets/{}"

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

        # Get collection data and image files
        self.data = self.get_page_data()
        self.files = self.data.get('files', []).copy()

        # Check for a recognized collection type
        self.page_type: CollectionType = self.get_collection_type()
        if not self.page_type:
            return

    def get_page_data(self) -> dict:
        """Returns a dictionary of data relating to this Mediux collection."""
        for script in self.soup.find_all('script'):
            if 'files' in script.text and 'set' in script.text and 'Set Link\\' not in script.text:
                return parse_json_string(script.text)['set']
        return {}

    def get_collection_type(self) -> CollectionType:
        """Returns the type of mediux page this is (movie or show)."""
        for f in self.files:
            if any([f["show_id"], f["show_id_backdrop"], f["episode_id"], f["season_id"], f["show_id"]]):
                if self.data.get('show'):
                    return MediaTypes.TVShow
        if self.data.get('collection') and self.data['collection'].get('movies'):
            return MediaTypes.MovieCollection
        return

    """
    * TV Objects
    """

    @default_prop
    def episode_data(self) -> dict[int, list]:
        """A dictionary of season numbers mapped to a list of episode IDs."""
        _episodes = {}
        for f in self.files:
            if f['fileType'] != 'title_card':
                continue
            _episode_id = (f.get('episode_id') or {}).get('id')
            _season_num = ((f.get("episode_id") or {}).get("season_id") or {}).get("season_number")
            if _season_num is None or _episode_id is None:
                continue
            _episodes.setdefault(_season_num, []).append((_episode_id, f['id']))
        return _episodes

    @default_prop
    def season_data(self) -> dict:
        """A dictionary of season ID's mapped to numbers and episodes."""
        return {
            n['id']: {
                'number': n['season_number'],
                'episodes': n['episodes']
            } for n in self.data['show']['seasons']
        }

    def get_tv_seasons(self) -> list[TVSeason]:
        """Returns a list of TVSeason objects."""
        seasons = []

        # Grab raw data for all seasons
        _seasons = [
            _f for _f in self.files
            if _f.get('season_id') and _f['season_id'].get('id')]
        [self.files.remove(n) for n in _seasons]

        # Build list of seasons
        for f in _seasons:

            # Get season data
            _season_id = f["season_id"]["id"]
            _season = self.season_data.get(_season_id)
            _season_num = _season['number']

            # Get poster and background
            background, poster = None, None
            if f['fileType'] == 'backdrop':
                background = self.url_formula.format(f['id'])
            else:
                poster = self.url_formula.format(f['id'])

            # Add season
            seasons.append(
                TVSeason(
                    number=_season_num,
                    url_poster=poster,
                    url_background=background,
                    source=MediaSources.Mediux,
                    episodes=self.get_tv_episodes(
                        _season_id, _season_num)
                ))
        return seasons

    def get_tv_episodes(self, season_id: str, season_num: int) -> list[TVEpisode]:
        """Returns a list of TVEpisode objects for a given TVSeason."""
        _season_data = self.season_data.get(season_id, {})
        if not _season_data:
            return []

        # Raw episodes
        _eps = {
            _e['id']: _e['episode_number']
            for _e in _season_data['episodes']}

        # Sorted episode URLs
        _episodes = dict(sorted({
            _eps[_id]: self.url_formula.format(_asset)
            for _id, _asset in self.episode_data.get(season_num, [])
        }.items()))

        # List of TVEpisode objects
        return [
            TVEpisode(
                number=num,
                url_title_card=url,
                source=MediaSources.Mediux
            ) for num, url in _episodes.items()
        ]

    """
    * Movie Objects
    """

    def get_movies(self) -> list[Movie]:
        """Returns a list of Movie objects."""
        movies: dict[str, Movie] = {}
        _movies = {m['id']: m for m in (self.data.get("collection") or {}).get("movies") or []}
        for f in self.files:

            # Get ID and title
            id_tmdb = (f.get("movie_id") or {}).get("id")
            title = _movies.get(id_tmdb)['title']
            if not title:
                continue

            # Get image URL
            url_poster, url_background = None, None
            url = self.url_formula.format(f['id'])
            if f['fileType'] == 'backdrop':
                url_background = url
            else:
                url_poster = url

            # Join existing if present
            if id_tmdb in movies:
                if not movies[id_tmdb].url_background and url_background:
                    movies[id_tmdb].url_background = url_background
                    continue
                if not movies[id_tmdb].url_poster and url_poster:
                    movies[id_tmdb].url_poster = url_poster
                    continue

            # Get release year
            year = _movies.get(id_tmdb)['release_date']
            if year is not None:
                year = int(year[:4])

            # Add movie
            movies[id_tmdb] = Movie(
                title=title,
                year=year,
                id_tmdb=id_tmdb,
                url_poster=url_poster,
                url_background=url_background,
                source=MediaSources.Mediux)

        # Join background and posters
        return [v for v in movies.values()]

    """
    * Collection Objects
    """

    def get_tv_show(self) -> TVShow:
        """Returns a TVShow object."""

        # Get show year
        show_data = self.data['show']
        try:
            year = int(show_data['first_air_date'][:4])
        except (IndexError, ValueError, KeyError, TypeError):
            year = None

        # Get show images
        remove, background, poster = [], None, None
        for i, f in enumerate(self.files):
            if f['fileType'] == 'backdrop':
                remove.append(i)
                background = self.url_formula.format(f['id'])
            elif f["show_id"] is not None:
                remove.append(i)
                poster = self.url_formula.format(f['id'])
        [self.files.pop(i) for i in remove]

        # Return TV Show object
        return TVShow(
            title=show_data['name'],
            year=year,
            seasons=self.get_tv_seasons(),
            url_background=background,
            url_poster=poster,
            id_tmdb=show_data['id'],
            source=MediaSources.Mediux
        )

    def get_movie_collection(self) -> MovieCollection:
        """Returns a MovieCollection object."""

        # Get movie collection title
        title = self.data["collection"]["collection_name"]

        # Get movie collection images
        remove, background, poster = [], None, None
        for i, f in enumerate(self.files):
            if f['fileType'] == 'backdrop':
                remove.append(i)
                background = self.url_formula.format(f['id'])
            elif f['fileType'] == 'poster' and f["movie_id"] is None:
                remove.append(i)
                poster = self.url_formula.format(f['id'])
        [self.files.pop(i) for i in remove]

        return MovieCollection(
            title=title,
            url_background=background,
            url_poster=poster,
            source=MediaSources.Mediux,
            movies=self.get_movies()
        )

    def get_collection(self) -> Optional[MovieCollection | TVShow]:
        """Check whether this is a Movie collection or a TV Show, then build and return the appropriate object."""
        if self.page_type is None:
            return logger.error('No main collection or show poster was found on this page!')
        if self.page_type == MediaTypes.TVShow:
            return self.get_tv_show()
        if self.page_type == MediaTypes.MovieCollection:
            return self.get_movie_collection()
