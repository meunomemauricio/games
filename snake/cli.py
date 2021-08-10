"""Application Command Line Interface."""

import click


@click.group()
def cli():
    """Application CLI object."""


@cli.command()
def run():
    print("Hello")
