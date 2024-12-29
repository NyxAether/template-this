from pathlib import Path


class Paths:
    def __init__(self, working_dir: Path) -> None:
        self.working_dir = working_dir.resolve()
        self.home_dir: Path = Path.home()
        self.cache_dir = self.home_dir / ".cache" / "template-this"
        self.tt_yml = self.cache_dir / "tt.yml"
        self.pyproject = self.cache_dir / "pyproject.toml"
