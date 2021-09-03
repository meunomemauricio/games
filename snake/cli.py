"""Application Command Line Interface."""

import click

from snake.experimental import MainApp as ExperimentalMainApp
from snake.main import MainApp


@click.group()
def cli():
    """Application CLI object."""


@cli.command()
def run():
    main = MainApp()
    main.execute()


@cli.command()
def experimental():
    ExperimentalMainApp().execute()
