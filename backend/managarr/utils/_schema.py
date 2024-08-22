"""
* Data Schemas
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
from omnitils.enums import StrConstant
from omnitils.schema import Schema

"""
* Enums
"""


class MediaSources(StrConstant):
    """Sources of media files."""
    Mediux: str = 'mediux'
    PosterDB: str = 'posterdb'


class MediaTypes(StrConstant):
    """Types of source media."""
    Movie = 'movie'
    MovieCollection = 'movie-collection'
    TVShow = 'tv-show'
    TVSeason = 'tv-season'
    TVEpisode = 'tv-episode'


"""
* Poster Schemas
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
* Movie Schemas
"""


class Movie(Schema):
    """Represents a movie scraped from ThePosterDB or Mediux."""
    title: str
    url_poster: Optional[str] = None
    url_background: Optional[str] = None
    year: Optional[int] = None
    id_tmdb: Optional[int] = None
    source: MediaSources


class MovieCollection(Schema):
    """Represents a movie collection scraped from ThePosterDB or Mediux."""
    title: str
    url_poster: Optional[str] = None
    url_background: Optional[str] = None
    movies: list[Movie]
    source: MediaSources


"""
* TV Schemas
"""


class TVEpisode(Schema):
    """Represents a TV show episode scraped from Mediux."""
    number: int
    url_title_card: Optional[str] = None
    source: MediaSources


class TVSeason(Schema):
    """Represents a TV show season scraped from Mediux."""
    number: int
    url_poster: Optional[str] = None
    url_background: Optional[str] = None
    source: MediaSources
    episodes: list[TVEpisode]


class TVShow(Schema):
    """Represents a TV show scraped from ThePosterDB or Mediux."""
    title: str
    url_poster: Optional[str] = None
    url_background: Optional[str] = None
    year: Optional[int] = None
    source: MediaSources
    seasons: list[TVSeason]
    id_tmdb: Optional[int] = None
