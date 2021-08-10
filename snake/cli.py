"""Application Command Line Interface."""

import click

from snake.main import MainApp


@click.group()
def cli():
    """Application CLI object."""


@cli.command()
def run():
    main = MainApp()
    main.execute()
