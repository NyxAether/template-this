import subprocess
from pathlib import Path

from ..settings import ProjectSettings
from . import DepManager


class PoetryManager(DepManager):

    def new(self, project_path: Path, settings: ProjectSettings) -> None:
        subprocess.run([settings.dep_manager_path, "new", project_path])

    def add(self, settings: ProjectSettings) -> None:
        if len(settings.librairies) > 0:
            subprocess.run(
                [
                    settings.dep_manager_path,
                    "add",
                    *[
                        library.name + library.version
                        for library in settings.librairies
                    ],
                    "--group",
                    "dev",
                ]
            )

    def install(self, settings: ProjectSettings) -> None:
        subprocess.run([settings.dep_manager_path, "install"])
