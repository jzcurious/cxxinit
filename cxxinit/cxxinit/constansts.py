from importlib.resources import files

CONFIG_ALLOWED_NAMES = ["cxxinit.yaml", "cxxinit.yml"]

RESOURCES = files("cxxinit.assets")

DIST_PATH = RESOURCES.joinpath("dist")
CMAKE_TEMPLATES_PATH = RESOURCES.joinpath("templates").joinpath("cmake")
SAMPLE_CONFIG_PATH = RESOURCES.joinpath("sample").joinpath("cxxinit.yml")


DEFAULT_CONFIG_DICT = {
    "cmake_version": "3.24",
    "std": 23,
    "cxx_flags": {
        "debug": "-Wall -pedantic -O0 -g -fsanitize=address",
        "release": "-Wall -pedantic -O3",
    },
}
