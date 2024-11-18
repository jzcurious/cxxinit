from pathlib import Path
import yaml
from constansts import *


class Project:
    def __init__(self, config_path: str | Path):
        self.config_dict = DEFAULT_CONFIG_DICT.copy()
        self.config_path = Path(config_path)
        with self.config_path.open() as f:
            self.config_dict.update(yaml.load(f, Loader=yaml.SafeLoader))
        self.path = Path(self.config_dict["root_path"])
        self.name = self.path.name
        self.std = self.config_dict["std"]
        self.cmake_version = self.config_dict["cmake_version"]
        self.cxx_flags = self.config_dict["cxx_flags"]
        self.subdirs = [
            Subdir(name, self, conf)
            for name, conf in self.config_dict["subdirs"].items()
        ]
        self.tree = self.config_dict.get("tree", None)
        self.fetch = self.config_dict.get("fetch", None)


class Subdir:
    def __init__(self, name: str, project: Project, config_dict_subdir: dict):
        self.config_dict = config_dict_subdir
        self.name = name
        self.path = project.path.joinpath(name)
        self.target_type = config_dict_subdir.get("target_type", None)
        self.sources_dir = config_dict_subdir.get("sources_dir", None)
        self.headers_dir = config_dict_subdir.get("headers_dir", None)
        self.build_cases = config_dict_subdir.get("build_cases", ["debug", "release"])
        self.prepend = config_dict_subdir.get("prepend", [])
        self.append = config_dict_subdir.get("append", [])
        if "deps" in config_dict_subdir:
            self.deps = [
                Dep(name, project, conf)
                for name, conf in config_dict_subdir["deps"].items()
            ]
        else:
            self.deps = []


class Dep:
    def __init__(self, name: str, project: Project, config_dict_dep: dict):
        self.config_dict = config_dict_dep
        self.name = name
        self.dep_type = config_dict_dep.get("dep_type", "subdir")
        self.repo = config_dict_dep.get("repo", None)
        self.tag = config_dict_dep.get("tag", "main")
        self.link_as = config_dict_dep.get("link_as", self.name)
        self.headers_path = None
        self.sources_path = None

        if self.dep_type == "subdir":
            subdir = project.config_dict["subdirs"][self.name]

            headers_dir = subdir.get("headers_dir", None)
            if headers_dir:
                self.headers_path = Path(
                    f"${{CMAKE_CURRENT_SOURCE_DIR}}/../{self.name}/{headers_dir}"
                )

            sources_dir = subdir.get("sources_dir", None)
            if sources_dir:
                self.sources_path = Path(
                    f"${{CMAKE_CURRENT_SOURCE_DIR}}/../{self.name}/{sources_dir}"
                )
