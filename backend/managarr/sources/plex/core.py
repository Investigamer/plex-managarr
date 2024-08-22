"""
* Retrieve Data from Plex
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
import yarl
from plexapi.server import PlexServer

"""
* Funcs
"""


def get_server(url: str, token: str, port: Optional[int | str] = None) -> PlexServer:
    """Return a PlexServer object using the provided credentials.

    Args:
        url (str): Plex server URL.
        port (int | str): Plex server port.
        token (str): Plex server token.

    Returns:
        A PlexServer object.
    """
    url = yarl.URL(url)
    if port:
        url = url.with_port(port)
    return PlexServer(
        baseurl=str(url),
        token=token,
        timeout=30)


def get_libraries(plex: PlexServer):
    """Return all libraries for a provided Plex server."""
    return [n for n in plex.library.sections()]
