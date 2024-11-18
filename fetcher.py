from model import Project
from pathlib import Path
from shutil import copytree, copy as copy_file


def find_content(name: str) -> Path | None:
    path = Path(name)

    if path.exists():
        return path

    path = Path("assets/dist").joinpath(name)

    if path.exists():
        return path


def fetch_all(project: Project) -> list[Path]:
    content = project.fetch

    found = []

    for item in content:
        if isinstance(item, dict):
            src_path = find_content(list(item.values())[0])
            dst_path = project.path.joinpath(list(item.keys())[0])
        else:
            src_path = find_content(item)
            dst_path = project.path.joinpath(item)

        if not src_path:
            continue
        else:
            found.append(src_path)

        if src_path.is_file():
            copy_file(src_path, dst_path)
        else:
            copytree(src_path, dst_path)

    return found
