"""Package Setup."""
from setuptools import find_packages, setup

setup(
    name="snake_game",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click==7.1.2",
        "pygame==2.0.1 ",
    ],
    extras_require={
        "dev": ["pre-commit"],
    },
    entry_points="""
        [console_scripts]
        snake=snake.cli:cli
    """,
)
