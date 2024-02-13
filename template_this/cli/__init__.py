import os
from pathlib import Path

import click

from template_this.paths import Paths
from template_this.project_builder import ProjectBuilder


@click.command(help="Create a new template following predefined settings")
@click.argument("project_path")
@click.option("--github", default="", help="ssh url to your github repository")
@click.option(
    "--no-cli",
    is_flag=True,
    show_default=True,
    default=False,
    help="Add this option if you don't want a cli alias in your pyproject.toml "
    "generated py poetry",
)
def main(project_path: str, github: str, no_cli: bool) -> None:
    paths = Paths(Path(os.getcwd()))

    builder = ProjectBuilder(
        project_path=Path(project_path), paths=paths, github=github, cli=not no_cli
    )
    builder.build()


if __name__ == "__main__":
    main()
