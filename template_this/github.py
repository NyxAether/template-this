import subprocess


class Github:

    def __init__(self, github: str) -> None:
        self._github = github

    def init(self) -> None:
        subprocess.run(["git", "init"])

    def add(self) -> None:
        subprocess.run(["git", "add", "."])

    def commit(self, msg: str = "Initial commit") -> None:
        subprocess.run(["git", "commit", "-m", msg])

    def add_remote(self) -> None:
        subprocess.run(["git", "remote", "add", "origin", self._github])
        subprocess.run(["git", "pull", "origin", "main"])
        subprocess.run(["git", "push", "-u", "origin", "main"])

    def push(self) -> None:
        subprocess.run(["git", "push"])

    def build(self) -> None:
        self.init()
        self.add()
        self.commit()
        if self._github != "":
            self.add_remote()
            # self.push()
