"""
* Plex Object Schemas
"""
from omnitils.schema import Schema

"""
* Schemas
"""


class EpisodeSchema(Schema):
    episode_number: int
    poster: str | None


class SeasonSchema(Schema):
    season_number: int
    poster: str | None
    background: str | None
    episodes: dict[int, str]  # Dictionary with episode number as key and poster as value


class ShowSchema(Schema):
    title: str
    poster: str | None
    background: str | None
    seasons: list[SeasonSchema]


class MovieSchema(Schema):
    title: str
    poster: str | None
    background: str | None


class MovieCollectionSchema(Schema):
    title: str
    poster: str | None
    background: str | None
    movies: list[MovieSchema]


class ShowCollectionSchema(Schema):
    title: str
    poster: str | None
    background: str | None
    shows: list[ShowSchema]
