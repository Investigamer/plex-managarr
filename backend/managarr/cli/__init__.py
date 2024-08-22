"""
* CLI Application
* Primarily used for testing and development.
"""
# Third Party Imports
import click

# Local Imports
from managarr.cli.generate import GenerateGroup


@click.group(
    name='managarr',
    commands={'get': GenerateGroup})
def ManagarrCLI():
    """CLI application entrypoint."""
    pass


# Export CLI Application
__all__ = ['ManagarrCLI']
