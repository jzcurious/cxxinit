from model import Project
from pathlib import Path
from shutil import copytree, copy as copy_file
from constansts import *


def find_content(name: str) -> tuple[str, Path | None]:
    path = Path(name)

    if path.exists():
        return name, path

    path = Path(DIST_PATH).joinpath(name)

    if path.exists():
        return name, path

    return name, None


def fetch_all(project: Project) -> tuple[list[Path], list[Path]]:
    content = project.fetch

    found = []
    not_found = []

    for item in content:
        if isinstance(item, dict):
            src_name, src_path = find_content(list(item.values())[0])
            dst_path = project.path.joinpath(list(item.keys())[0])
        else:
            src_name, src_path = find_content(item)
            dst_path = project.path.joinpath(item)

        if not src_path:
            not_found.append(src_name)
            continue
        else:
            found.append(src_path)

        if src_path.is_file():
            copy_file(src_path, dst_path)
        else:
            copytree(src_path, dst_path)

    return found, not_found
