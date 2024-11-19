from cxxinit.model import Project
import cxxinit.constansts as constansts
from pathlib import Path
from shutil import copytree, copy as copy_file
from importlib.resources.abc import Traversable
from importlib.readers import MultiplexedPath


def find_content(name: str) -> tuple[str, None | Traversable]:
    path = Path(name)

    if path.exists():
        return name, path

    try:
        resource = constansts.DIST_PATH.joinpath(name)
        return name, resource
    except ModuleNotFoundError:
        pass

    return name, None


# def fetch_all(project: Project) -> tuple[list[Path], list[Path]]:
#     content = project.fetch

#     found = []
#     not_found = []

#     for item in content:
#         if isinstance(item, dict):
#             src_name, src_path = find_content(list(item.values())[0])
#             dst_path = project.path.joinpath(list(item.keys())[0])
#         else:
#             src_name, src_path = find_content(item)
#             dst_path = project.path.joinpath(item)

#         if not src_path:
#             not_found.append(src_name)
#             continue

#         found.append(src_path)

#         if isinstance(src_path, Path):
#             if src_path.is_file():
#                 copy_file(src_path, dst_path)
#             else:
#                 copytree(src_path, dst_path)
#             continue

#         if src_path.is_file():
#             pass

#     return found, not_found


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

        if isinstance(src_path, Path):
            if src_path.is_file():
                copy_file(src_path, dst_path)
            else:
                copytree(src_path, dst_path)
            continue

        if isinstance(src_path, MultiplexedPath):
            if src_path.is_file():
                with open(dst_path, "wb") as dst:
                    dst.write(src_path.read_bytes())
            else:
                not_found.append(src_name)

    return found, not_found
