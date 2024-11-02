from explorer import Explorer
from structure import Structure
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

if __name__ == "__main__":
    e = Explorer(Path("/home/void/Projects/cxxinit/cxxinit.yml"))
    print(e.root_path)
    s = Structure(e.root_path, *e.subdirs_paths)
    s.apply()

    env = Environment(
        loader=FileSystemLoader("./assets/templates/cmake"),
    )

    template = env.get_template("main.txt")
