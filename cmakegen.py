from model import Project
from jinja2 import Environment, FileSystemLoader


class CmakeGen:
    __jenv = Environment(loader=FileSystemLoader("assets/templates/cmake"))

    @staticmethod
    def generate(project: Project):
        CmakeGen.__generate_main(project)

    @staticmethod
    def __generate_main(project: Project):
        t = CmakeGen.__jenv.get_template("main.txt")

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

        s = t.render(
            project_name=project.name,
            cmake_version=project.cmake_version,
            std=project.std,
            build_cases=build_cases,
        )

        print(s)
        return s
