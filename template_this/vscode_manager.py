from pathlib import Path

from jinja2 import Environment

from template_this.paths import Paths
from template_this.settings import ProjectSettings


class VSCodeManager:
    def __init__(self) -> None:
        pass

    def _template_and_copy(
        self,
        template_path: Path,
        project_path: Path,
        paths: Paths,
        template_kwargs: dict[str, str],
    ) -> None:
        (project_path / template_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(paths.cache_dir / template_path, "r") as template_cfg, open(
                project_path / template_path, "w"
            ) as launch:
                template = Environment().from_string(template_cfg.read())
                launch.write(template.render(**template_kwargs))
        except FileNotFoundError:
            print(
                f"File {paths.cache_dir / template_path} not found. "
                "No config file added."
            )

    def build(
        self, project_path: Path, settings: ProjectSettings, paths: Paths, cli_name: str
    ) -> None:
        if settings.vscode_config is None:
            return
        launch_path = settings.vscode_config.launch_config
        settings_path = settings.vscode_config.settings_config
        makefile_paths = settings.vscode_config.makefile_config

        if launch_path:
            self._template_and_copy(
                launch_path, project_path, paths, {"cli_name": cli_name}
            )
        if settings_path:
            self._template_and_copy(
                settings_path,
                project_path,
                paths,
                {},
            )
        if makefile_paths:
            for makefile_path in makefile_paths:
                self._template_and_copy(makefile_path, project_path, paths, {"project_src":project_path.name.replace("-", "_")})
