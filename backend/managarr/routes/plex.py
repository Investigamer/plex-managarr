"""
* Plex API Endpoints
"""
# Standard Library
import yarl

# Third Party Imports
from ninja import Router
from plexapi.server import PlexServer

# Local Imports
from managarr.sources.plex.schemas import MovieSchema, ShowSchema, ShowCollectionSchema, MovieCollectionSchema
from managarr.apps import ManagarrConfig

# API objects
PlexAPI: PlexServer = ManagarrConfig.PlexAPI
api = Router()


def get_transcode_url(url: str, token: str):
    url = yarl.URL('https://plex.texflix.org/photo/:/transcode').with_query({
        'width': 360,
        'height': 540,
        'minSize': 1,
        'upscale': 1,
        'url': f'{url}?X-Plex-Token={token}',
        'X-Plex-Token': token
    })


@api.get("/movies/{library_name}", response=list[MovieSchema])
def get_movies_in_library(request, library_name: str):
    library = PlexAPI.library.section(library_name)
    movies = []
    for movie in library.all():
        movies.append({
            "title": movie.title,
            "poster": movie.thumbUrl,
            "background": movie.artUrl
        })
    return movies


@api.get("/shows/{library_name}", response=list[ShowSchema])
def get_shows_in_library(request, library_name: str):
    library = PlexAPI.library.section(library_name)
    shows = []
    for show in library.all():
        seasons = []
        for season in show.seasons():
            episodes = {episode.index: episode.thumb for episode in season.episodes()}
            seasons.append({
                "season_number": season.index,
                "poster": season.thumbUrl,
                "background": season.artUrl,
                "episodes": episodes
            })
        shows.append({
            "title": show.title,
            "poster": show.thumbUrl,
            "background": show.artUrl,
            "seasons": seasons
        })
    return shows


@api.get("/collections/movie/{library_name}", response=list[MovieCollectionSchema])
def get_movie_collections(request, library_name: str):
    library = PlexAPI.library.section(library_name)
    collections = []
    for collection in library.collections():
        movies = []
        for movie in collection.children:
            if not movie.thumb:
                print(movie.title, 'missing thumbnail!')
            if not movie.art:
                print(movie.title, 'missing background!')
            movies.append({
                "title": movie.title,
                "poster": PlexAPI.transcodeImage(movie.thumbUrl, height=540, width=360, background='000000'),
                "background": movie.artUrl
            })
        if not collection.thumb:
            print(collection.title, 'missing thumbnail!')
        if not collection.art:
            print(collection.title, 'missing background!')
        collections.append({
            "title": collection.title,
            "poster": PlexAPI.transcodeImage(collection.thumbUrl, height=540, width=360),
            "background": collection.artUrl,
            "movies": movies
        })
    return collections


@api.get("/collections/show/{library_name}", response=list[ShowCollectionSchema])
def get_show_collections(request, library_name: str):
    library = PlexAPI.library.section(library_name)
    collections = []
    for collection in library.collections():
        shows = []
        for show in collection.children:
            seasons = []
            for season in show.seasons():
                episodes = {episode.index: episode.thumb for episode in season.episodes()}
                seasons.append({
                    "season_number": season.index,
                    "poster": season.thumbUrl,
                    "background": season.artUrl,
                    "episodes": episodes
                })
            shows.append({
                "title": show.title,
                "poster": show.thumbUrl,
                "background": show.artUrl,
                "seasons": seasons
            })
        collections.append({
            "title": collection.title,
            "poster": collection.thumbUrl,
            "background": collection.artUrl,
            "shows": shows
        })
    return collections
