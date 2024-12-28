from typing import TYPE_CHECKING

from . import DepManager

if TYPE_CHECKING:
    from pathlib import Path

    from ..paths import Paths


class UVManager(DepManager):
    def _create_project(self, project_path: Path) -> Path:
        return project_path

    def _copy_configs(self, project_path: Path, paths: Paths) -> None:
        raise NotImplementedError

    def _create_cli(self, project_path: Path, paths: Paths, cli_name: str) -> None:
        raise NotImplementedError

    def build(self, project_path: Path, paths: Paths, cli_name: str) -> Path:
        return super().build(project_path, paths, cli_name)
