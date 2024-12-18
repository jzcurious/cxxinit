# cxxinit

A utility for initializing a C++ project. Based on CMake.

### Installation

```bash
pip install "git+https://github.com/jzcurious/cxxinit.git"
```

### Using

1. Create a configuration file (cxxinit.yml) in the directory of the future project or in any other directory.
2. Type in terminal: "cxxinit -c /path/to/cxxinit.yml".
3. Enjoy.


### Config sample

```yaml
# A sample configuration (assets/samples/cxxinit.yml)

root_path: "/home/void/Projects/myproj" # is required
cmake_version: 3.24...3.30
std: 23

tree:
  - myproj-lib:
      - include:
          - myproj:
              - myproj.hpp
              - some_header.hpp
          - some_nested_folder: null
      - some_empty_folder: null

  - tests:
      - src:
          - tests.cpp
          - some_src.cpp

  - benchmarks:
      - src:
          - benchmarks.cpp
          - some_src.cpp

  - security:
      - src:
          - security.cpp
          - some_src.cpp

fetch:
  - .gitignore
  - .clang-format: clang-format
  - some_folder/some_file.txt: /home/void/some_file.txt

subdirs: # is required
  myproj-lib:
    target_type: interface
    headers_dir: include
    alias: myproj
    build_cases:
      - release
      - debug

  tests:
    target_type: executable
    sources_dir: src
    deps:
      myproj-lib:
        dep_type: subdir
        link_as: myproj
      googletest:
        dep_type: git
        repo: https://github.com/google/googletest.git
        tag: v1.15.2
        link_as: GTest::gtest_main
    build_cases:
      - release
    prepend:
      - include(GoogleTest)
    append:
      - enable_testing()
      - gtest_discover_tests(myproj-tests)

  benchmarks:
    target_type: executable
    sources_dir: src
    deps:
      myproj-lib:
        dep_type: subdir
        link_as: myproj
      benchmark:
        dep_type: git
        repo: https://github.com/google/benchmark.git
        tag: v1.9.0
        link_as: benchmark::benchmark
    build_cases:
      - release

  security:
    target_type: executable
    sources_dir: src
    deps:
      myproj-lib:
        dep_type: subdir
        link_as: myproj
    build_cases:
      - debug

cxx_flags:
  debug: "-Wall -pedantic -O0 -g -fsanitize=address"
  release: "-Wall -pedantic -O3"
```
