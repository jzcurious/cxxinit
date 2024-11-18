from model import Project
from jinja2 import Environment, FileSystemLoader
from constansts import *


_jenv = Environment(loader=FileSystemLoader(CMAKE_TEMPLATES_PATH))


def generate_lists(project: Project):
    _generate_main(project)
    _generate_subdirs(project)


def _remove_empty_lines(s: str) -> str:
    return "\n".join([line for line in s.split("\n") if line])


def _generate_main(project: Project):
    build_cases_names = set()
    for subdir in project.subdirs:
        build_cases_names |= set(subdir.build_cases)

    build_cases = {
        key: {"subdirs": [], "flags": project.cxx_flags[key]}
        for key in build_cases_names
    }

    for subdir in project.subdirs:
        for case in subdir.build_cases:
            build_cases[case]["subdirs"].append(subdir.name)

    with project.path.joinpath("CMakeLists.txt").open("w") as f:
        s = _jenv.get_template("main.txt").render(
            project=project,
            build_cases=build_cases,
        )
        f.write(
            _remove_empty_lines(s),
        )


def _generate_subdirs(project: Project):
    t = _jenv.get_template("subdir.txt")

    for subdir in project.subdirs:
        with subdir.path.joinpath("CMakeLists.txt").open("w") as f:
            s = t.render(
                project=project,
                subdir=subdir,
                need_fetch_content=any([d.dep_type == "git" for d in subdir.deps]),
            )
            f.write(
                _remove_empty_lines(s),
            )
