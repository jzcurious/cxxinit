import yaml
from pathlib import Path


class Explorer:
    def __init__(self, config_path):
        self.__config_path = config_path

        with config_path.open("r") as f:
            self.__config = yaml.load(f, Loader=yaml.SafeLoader)

    @property
    def config(self):
        return self.__config

    @property
    def root_path(self):
        return Path(self.__config["root_path"])

    @property
    def project_name(self):
        return self.root_path.name

    @property
    def std_version(self):
        return self.__config["std_version"]

    @property
    def subdirs_paths(self):
        return [self.root_path.joinpath(k) for k in self.__config["subdirs"].keys()]

    @property
    def subdirs(self):
        return self.__config["subdirs"]

    @property
    def cxx_flags(self):
        return self.__config["cxx_flags"]
