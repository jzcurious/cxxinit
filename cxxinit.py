from model import Project
import treemaker
import cmakegen
import fetcher
from argparse import ArgumentParser


if __name__ == "__main__":
    proj = Project("cxxinit.yml")

    if not treemaker.make_tree(proj, True):
        print(
            "Failed: directory is not empty. "
            "Use the -a option to add project files to an existing directory. "
            "Or manually delete the old version of the project."
        )
        exit(1)

    cmakegen.generate_lists(proj)

    found = fetcher.fetch_all(proj)
