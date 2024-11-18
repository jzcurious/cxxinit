from model import Project
from pathlib import Path
from shutil import copytree, copy as copy_file


def find_content(name: str) -> Path | None:
    path = Path(name)

    if path.exists():
        return path

    path = Path("dist").joinpath(name)

    if path.exists():
        return path


def fetch_all(project: Project):
    content = project.fetch

    for item in content:
        src_path = find_content(list(item.values())[0])
        dst_path = Path(list(item.keys())[0])

        if not src_path:
            continue

        if src_path.is_file:
            copy_file(src_path, dst_path)
        else:
            copytree(src_path, dst_path)
