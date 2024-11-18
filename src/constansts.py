CONFIG_ALLOWED_NAMES = ["cxxinit.yaml", "cxxinit.yml"]
DIST_PATH = "assets/dist"
CMAKE_TEMPLATES_PATH = "assets/templates/cmake"
SAMPLE_CONFIG_PATH = "assets/sample/cxxinit.yml"


DEFAULT_CONFIG_DICT = {
    "cmake_version": "3.24",
    "std": 23,
    "cxx_flags": {
        "debug": "-Wall -pedantic -O0 -g -fsanitize=address",
        "release": "-Wall -pedantic -O3",
    },
}
