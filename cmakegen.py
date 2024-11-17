from model import Project
from jinja2 import Environment, FileSystemLoader


class CmakeGen:
    __jenv = Environment(loader=FileSystemLoader("assets/templates/cmake"))

    @staticmethod
    def generate(project: Project):
        CmakeGen.__generate_main(project)
        CmakeGen.__generate_subdirs(project)

    @staticmethod
    def __remove_empty_lines(s: str) -> str:
        return "\n".join([line for line in s.split("\n") if line])

    @staticmethod
    def __generate_main(project: Project):
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
            s = CmakeGen.__jenv.get_template("main.txt").render(
                project=project,
                build_cases=build_cases,
            )
            f.write(
                CmakeGen.__remove_empty_lines(s),
            )

    @staticmethod
    def __generate_subdirs(project: Project):
        t = CmakeGen.__jenv.get_template("subdir.txt")

        for subdir in project.subdirs:
            with subdir.path.joinpath("CMakeLists.txt").open("w") as f:
                s = t.render(
                    project=project,
                    subdir=subdir,
                    need_fetch_content=any([d.dep_type == "git" for d in subdir.deps]),
                )
                f.write(
                    CmakeGen.__remove_empty_lines(s),
                )
