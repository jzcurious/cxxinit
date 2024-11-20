from cxxinit.model import Project
import cxxinit.constansts as constansts
from pathlib import Path, PosixPath
from shutil import copytree, copy as copy_file


def find_content(name: str) -> tuple[str, None | Path]:
    path = Path(name)

    if path.exists():
        return name, path

    if name[0] == ".":
        name = name[1:]

    try:
        resource = constansts.DIST_PATH.joinpath(name)
        if isinstance(resource, Path):
            if resource.exists():
                return name, resource
    except ModuleNotFoundError:
        pass

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

        if src_path.is_file():
            copy_file(src_path, dst_path)
        else:
            copytree(src_path, dst_path)
        continue

    return found, not_found
