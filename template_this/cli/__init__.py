import os
from pathlib import Path

import click

from template_this.paths import Paths
from template_this.project_builder import ProjectBuilder


@click.command(help="Create a new template following predefined settings")
@click.argument("project_path")
@click.option("--github", default="", help="ssh url to your github repository")
@click.option(
    "--cli-name",
    show_default=True,
    default="False",
    help=(
        "Specify if you want a cli alias in your pyproject.toml."
        "If none are specified, no cli alias nor cli config will be generated"
    ),
)
def main(project_path: str, github: str, cli_name: str) -> None:
    paths = Paths(Path(os.getcwd()))

    builder = ProjectBuilder(
        project_path=Path(project_path), paths=paths, github=github, cli_name=cli_name
    )
    builder.build()


if __name__ == "__main__":
    main()
