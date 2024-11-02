from pathlib import Path
import yaml


class Project:
    def __init__(self, config_path_str: str):
        self.config_path = Path(config_path_str)
        self.config_dict = {}
        with self.config_path.open() as f:
            self.config_dict.update(yaml.load(f, Loader=yaml.SafeLoader))
        self.path = Path(self.config_dict["root_path"])
        self.name = self.path.name
        self.std = self.config_dict.get("std", 20)
        self.cmake_version = self.config_dict.get("cmake_version", "3.24...3.30")
        self.cxx_flags = self.config_dict.get(
            "cxx_flags",
            {
                "debug": "-Wall -pedantic -O0 -g -fsanitize=address",
                "release": "-Wall -pedantic -O3",
            },
        )
        self.subdirs = [
            Subdir(name, self.path, conf)
            for name, conf in self.config_dict["subdirs"].items()
        ]


class Subdir:
    def __init__(self, name: str, project_path: Path, config_dict_subdir: dict):
        self.name = name
        self.path = project_path.joinpath(name)
        self.target_type = config_dict_subdir.get("target_type", "lib_static")
        self.sources_dir = config_dict_subdir.get("sources_dir", None)
        self.headers_dir = config_dict_subdir.get("headers_dir", None)
        self.build_cases = config_dict_subdir.get("build_cases", ["debug", "release"])
        if "deps" in config_dict_subdir:
            self.deps = [
                Dep(name, conf) for name, conf in config_dict_subdir["deps"].items()
            ]
        else:
            self.deps = []


class Dep:
    def __init__(self, name: str, config_dict_dep: dict):
        self.name = name
        self.subdir = config_dict_dep.get("subdir", False)
        self.repo = config_dict_dep.get("repo", None)
        self.tag = config_dict_dep.get("tag", "main")
        self.link_as = config_dict_dep.get("link_as", None)
