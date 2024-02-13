import os
import subprocess
from pathlib import Path
from shutil import copyfile

from jinja2 import Environment

from template_this.paths import Paths
from template_this.settings import ProjectSettings


class PoetryManager(object):
    def __init__(self, settings: ProjectSettings) -> None:
        self.settings = settings

    def build(self, project_path: Path, paths: Paths, cli: bool) -> Path:
        if project_path.exists():
            raise FileExistsError(
                f"Project path {project_path} already exists. Aborting."
            )
        # Create project
        subprocess.run([self.settings.poetry_path, "new", project_path])
        project_path = project_path.resolve()
        os.chdir(project_path)
        # Add libraries
        if len(self.settings.librairies) > 0:
            subprocess.run(
                [
                    self.settings.poetry_path,
                    "add",
                    *[
                        library.name + library.version
                        for library in self.settings.librairies
                    ],
                ]
            )
        # Add config files for tools
        for library in self.settings.librairies:
            if library.config is not None:
                config_file = Path(library.config)
                if (paths.cache_dir / config_file).exists():
                    copyfile(paths.cache_dir / config_file, project_path / config_file)
                else:
                    print(
                        f"Config file {paths.cache_dir / config_file} not found. "
                        f"No config file added for {library.name}"
                    )

        # Update pyproject.toml
        if paths.pyproject.exists():
            with open(paths.pyproject, "r") as config, open(
                project_path / "pyproject.toml", "a"
            ) as toml:
                template = Environment().from_string(config.read())
                toml.write("\n\n")
                toml.write(template.render(project_name=project_path.name))
        # Install dependencies
        subprocess.run([self.settings.poetry_path, "install"])

        return project_path
