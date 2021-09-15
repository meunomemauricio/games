"""Application Command Line Interface."""

import click

from snake.experimental import MainApp as ExperimentalMainApp
from snake.main import MainApp


@click.group()
def cli():
    """Application CLI object."""


@cli.command()
@click.option("-f", "--fps/--no-fps", default=False)
@click.option("-g", "--grid/--no-grid", default=True)
def run(fps: bool, grid: bool):
    MainApp(grid=grid, show_fps=fps).run()


@cli.command()
@click.option("-b", "--blueprint", default="blocks")
@click.option("-d", "--debug/--no-debug", default=False)
@click.option("-f", "--fps/--no-fps", default=False)
@click.option("-g", "--grid/--no-grid", default=False)
def experimental(blueprint: str, debug: bool, fps: bool, grid: bool):
    ExperimentalMainApp(
        bp_name=blueprint, debug=debug, grid=grid, show_fps=fps
    ).run()
