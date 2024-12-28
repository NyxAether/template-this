import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from template_this.paths import Paths
    from template_this.settings import ProjectSettings


@dataclass
class DepManager(ABC):
    _settings: ProjectSettings

    @abstractmethod
    def _create_project(self, project_path: Path) -> Path:
        raise NotImplementedError

    @abstractmethod
    def _copy_configs(self, project_path: Path, paths: Paths) -> None:
        raise NotImplementedError

    @abstractmethod
    def _create_cli(self, project_path: Path, paths: Paths, cli_name: str) -> None:
        raise NotImplementedError

    def build(self, project_path: Path, paths: Paths, cli_name: str) -> Path:
        if project_path.exists():
            raise FileExistsError(
                f"Project path {project_path} already exists. Aborting."
            )
        # Create project
        project_path = self._create_project(project_path)

        # Add config files for tools
        self._copy_configs(project_path, paths)

        # Update pyproject.toml
        self._create_cli(project_path, paths, cli_name)

        # Install dependencies
        subprocess.run([self._settings.dep_manager_path, "install"])

        return project_path
