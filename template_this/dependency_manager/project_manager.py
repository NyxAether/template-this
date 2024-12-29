import os
from pathlib import Path
from shutil import copyfile

from jinja2 import Environment

from ..paths import Paths
from ..settings import ProjectSettings
from . import DepManager
from .poetry_manager import PoetryManager
from .uv_manager import UVManager


class ProjectManager:
    def __init__(self, settings: ProjectSettings) -> None:
        self._settings = settings

    def _create_project(self, project_path: Path, dep_manager: DepManager) -> Path:
        dep_manager.new(project_path, self._settings)
        project_path = project_path.resolve()
        os.chdir(project_path)
        # Add libraries
        dep_manager.add(self._settings)

        return project_path

    def _copy_configs(self, project_path: Path, paths: Paths) -> None:
        for library in self._settings.librairies:
            if library.config is not None:
                config_file = Path(library.config)
                if (paths.cache_dir / config_file).exists():
                    copyfile(paths.cache_dir / config_file, project_path / config_file)
                else:
                    print(
                        f"Config file {paths.cache_dir / config_file} not found. "
                        f"No config file added for {library.name}"
                    )

    def _create_cli(self, project_path: Path, paths: Paths, cli_name: str) -> None:
        if cli_name and paths.pyproject.exists():
            print(f"Updating {project_path.name.replace('-', '_')}")
            with (
                open(paths.pyproject) as config,
                open(project_path / "pyproject.toml", "a") as toml,
            ):
                template = Environment().from_string(config.read())
                toml.write("\n\n")
                toml.write(
                    template.render(
                        project_name=project_path.name.replace("-", "_"),
                        cli_name=cli_name,
                    )
                )
            src_file = project_path.name.replace("-", "_")
            cli_path = project_path / src_file / "cli" / "__init__.py"
            cli_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cli_path, "w") as cli_file:
                cli_file.write(
                    "def main() -> None:\n"
                    "    pass\n\n"
                    "if __name__ == '__main__':\n"
                    "    main()"
                )

    def build(self, project_path: Path, paths: Paths, cli_name: str) -> Path:
        if project_path.exists():
            raise FileExistsError(
                f"Project path {project_path} already exists. Aborting."
            )
        # Get manager
        dep_manager_path = Path(self._settings.dep_manager_path)
        manager = dep_manager_path.stem
        if manager == "poetry":
            dep_manager: DepManager = PoetryManager()
        elif manager == "uv":
            dep_manager = UVManager()
        else:
            raise ValueError(f"Unknown dependency manager {manager}")
        # Create project
        project_path = self._create_project(project_path, dep_manager)
        # Add config files for tools
        self._copy_configs(project_path, paths)

        # Update pyproject.toml
        self._create_cli(project_path, paths, cli_name)
        # Install dependencies
        dep_manager.install(self._settings)

        return project_path
