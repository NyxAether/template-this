from pathlib import Path
from shutil import copyfile

from jinja2 import Environment

from template_this.paths import Paths
from template_this.settings import ProjectSettings


class VSCodeManager:
    def __init__(self) -> None:
        pass

    def build(
        self, project_path: Path, settings: ProjectSettings, paths: Paths, cli: bool
    ) -> None:
        if settings.vscode_config is None:
            return
        launch_path = settings.vscode_config.launch_config
        settings_path = settings.vscode_config.settings_config

        if launch_path is not None:
            (project_path / launch_path).parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(paths.cache_dir / launch_path, "r") as template_cfg, open(
                    project_path / launch_path, "w"
                ) as launch:
                    template = Environment().from_string(template_cfg.read())
                    launch.write(template.render(cli=cli))
            except FileNotFoundError:
                print(
                    f"File {paths.cache_dir / launch_path} not found. "
                    "No launch config added."
                )

        if settings_path is not None:
            (project_path / settings_path).parent.mkdir(parents=True, exist_ok=True)
            try:
                copyfile(paths.cache_dir / settings_path, project_path / settings_path)
            except FileNotFoundError:
                print(
                    f"File {paths.cache_dir / settings_path} not found. "
                    "No settings config added."
                )
