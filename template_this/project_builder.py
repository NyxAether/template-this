import os
from pathlib import Path

import yaml

from template_this.github import Github
from template_this.paths import Paths
from template_this.poetry_manager import PoetryManager
from template_this.settings import ProjectSettings
from template_this.vscode_manager import VSCodeManager


class ProjectBuilder:
    def __init__(
        self, project_path: Path, paths: Paths, github: str, cli: bool
    ) -> None:
        self._project_path = project_path
        self._paths = paths
        self._github = github
        self._cli = cli

    def build(self) -> None:
        poetry_data = yaml.safe_load(self._paths.poetry_yml.read_text())

        settings = ProjectSettings.model_validate(poetry_data)

        poetry_manager = PoetryManager(settings)
        self._project_path = poetry_manager.build(
            self._project_path, self._paths, self._cli
        )
        os.chdir(self._project_path)

        vscode_manager = VSCodeManager()
        vscode_manager.build(self._project_path, settings, self._paths, self._cli)

        github_manager = Github(self._github)
        github_manager.build()
