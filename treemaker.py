from model import Project
from constansts import *
from pathlib import Path
from os import listdir


def _check_root_dir(path: Path, add=False) -> bool:
    if path.exists() and not add:
        ls = listdir(path)

        if len(ls) == 0:
            return True

        if (len(ls) == 1) and (ls[0] in CONFIG_ALLOWED_NAMES):
            return True

        return False

    return True


def _prepare_tree(root_path: Path, tree: list):
    root_path.mkdir(exist_ok=True, parents=True)

    if not tree:
        return

    for item in tree:
        if isinstance(item, dict):
            dirname = list(item.keys())[0]
            path = root_path.joinpath(dirname)
            content = item[dirname]
            _prepare_tree(path, content)

        if isinstance(item, str):
            path = root_path.joinpath(item)
            path.write_text("", encoding="utf-8")


def _make_subdirs(project: Project):
    for subdir in project.subdirs:
        if subdir.headers_dir:
            subdir.path.joinpath(subdir.headers_dir).mkdir(parents=True, exist_ok=True)

        if subdir.sources_dir:
            subdir.path.joinpath(subdir.sources_dir).mkdir(parents=True, exist_ok=True)


def make_tree(project: Project, add=False) -> bool:
    if not _check_root_dir(project.path, add):
        return False

    _prepare_tree(project.path, project.tree)
    _make_subdirs(project)

    return True
