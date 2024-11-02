from pathlib import Path
from model import Project
from os import listdir
from shutil import rmtree


class DirsMaker:
    @staticmethod
    def make(project: Project, force=False):
        if force:
            DirsMaker.__remove_old(project.path)

        project.path.mkdir(exist_ok=True, parents=True)

        try:
            for subdir in project.subdirs:
                if subdir.headers_dir:
                    subdir.path.joinpath(subdir.headers_dir).mkdir(parents=True)
                if subdir.sources_dir:
                    subdir.path.joinpath(subdir.sources_dir).mkdir(parents=True)
        except FileExistsError:
            print(
                "Failed: directory is not empty. Use option -f to remove old version."
            )
            return False

        return True

    @staticmethod
    def __remove_old(root_path: Path):
        for item in listdir(root_path):
            if item == "cxxinit.yml":
                continue

            path = root_path.joinpath(item)

            if path.is_file():
                path.unlink()
                continue

            if path.is_dir():
                rmtree(path)
