import shutil
import subprocess
from pathlib import Path

from ..settings import ProjectSettings
from . import DepManager


class UVManager(DepManager):

    def new(self, project_path: Path, settings: ProjectSettings) -> None:
        subprocess.run([settings.dep_manager_path, "init", "--package", project_path])
        project_path = project_path.resolve()
        src_folder = project_path.name.replace("-", "_")
        shutil.move(project_path / "src" / src_folder, project_path)
        shutil.rmtree(project_path / "src")

    def add(self, settings: "ProjectSettings") -> None:
        if len(settings.librairies) > 0:
            subprocess.run(
                [
                    settings.dep_manager_path,
                    "add",
                    *[
                        library.name + library.version
                        for library in settings.librairies
                    ],
                    "--dev",
                ]
            )

    def install(self, settings: "ProjectSettings") -> None:
        subprocess.run([settings.dep_manager_path, "sync"])
