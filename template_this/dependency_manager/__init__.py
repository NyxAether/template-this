from abc import ABC, abstractmethod
from pathlib import Path

from ..settings import ProjectSettings


class DepManager(ABC):

    @abstractmethod
    def new(self, project_path: Path, settings: ProjectSettings) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, settings: ProjectSettings) -> None:
        raise NotImplementedError

    @abstractmethod
    def install(self, settings: ProjectSettings) -> None:
        raise NotImplementedError
