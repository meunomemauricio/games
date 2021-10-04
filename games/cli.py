"""Application Command Line Interface."""

import click

from games.projectile import MainApp as ProjectileMainApp
from games.snake.main import MainApp as SnakeMainApp


@click.group()
def cli():
    """Application CLI object."""


@cli.command()
@click.option("-d", "--debug/--no-debug", default=False)
def snake(debug: bool):
    SnakeMainApp(debug=debug).run()


@cli.command()
@click.option("-b", "--blueprint", default="blocks")
@click.option("-d", "--debug/--no-debug", default=False)
@click.option("-f", "--fps/--no-fps", default=False)
@click.option("-g", "--grid/--no-grid", default=False)
def projectile(blueprint: str, debug: bool, fps: bool, grid: bool):
    ProjectileMainApp(
        bp_name=blueprint, debug=debug, grid=grid, show_fps=fps
    ).run()
