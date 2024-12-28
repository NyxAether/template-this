from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class Library(BaseModel):
    name: str
    version: str = ""
    config: Optional[Path] = None


class VSCodeConfig(BaseModel):
    launch_config: Optional[Path] = None
    settings_config: Optional[Path] = None
    makefile_config: Optional[list[Path]] = None


class ProjectSettings(BaseModel):
    dep_manager_path: str = "poetry"
    librairies: list[Library]
    vscode_config: Optional[VSCodeConfig] = None
