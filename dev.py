from explorer import Explorer
from pathlib import Path

if __name__ == "__main__":
    e = Explorer(Path("/home/void/Projects/cxxinit/cxxinit.yml"))
    print(e.subdirs_paths)
    print(e.root_path)
    print(e.project_name)
    print(e.std_version)
    print(e.cxx_flags)
    print(e.subdirs)
