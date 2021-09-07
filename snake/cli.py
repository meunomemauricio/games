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
@click.option("-b", "--blueprint", default="blocks")
@click.option("-d", "--debug/--no-debug", default=False)
@click.option("-g", "--grid/--no-grid", default=False)
def experimental(blueprint: str, debug: bool, grid: bool):
    ExperimentalMainApp(bp_name=blueprint, debug=debug, grid=grid).execute()
