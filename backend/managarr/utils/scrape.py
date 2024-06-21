"""
* Scraping Utilities
"""
# Standard Library Imports
import json
from typing import Optional

# Third Party Imports
import requests
import yarl
from bs4 import BeautifulSoup
from omnitils.fetch import request_header_default


def get_page_soup(
    url: str | yarl.URL,
    header: Optional[dict] = None,
    ignore_status_code: bool = False
):
    """Get a qualified BeautifulSoup object from a ThePosterDB page."""
    header = header or request_header_default.copy()
    with requests.get(url, headers=header) as r:

        # Load page into BS4
        if r.status_code == 200 or ignore_status_code:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup

        # Unable to retrieve page
        r.raise_for_status()


def parse_json_string(input_string: str):
    """Parse an object string from scraped javascript, return a dict.

    Args:
        input_string: Object string from scraped javascript.

    Returns:
        A dict representing the scraped object.
    """

    # Format string for parsing
    st = (input_string
          .replace('\\\\\\\"', "")
          .replace("\\", "")
          .replace("u0026", "&"))

    # Parse string into JSON data
    index_start, index_end = st.find('{'), st.rfind('}')
    data = st[index_start:index_end + 1]
    return json.loads(data)
