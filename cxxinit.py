from model import Project
import treemaker
import cmakegen
import fetcher
from argparse import ArgumentParser
from constansts import *
from pathlib import Path


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="specify the path to configure file",
    )

    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="add files to existing project",
    )

    args = parser.parse_args()
    config_path = Path(args.config)

    if not (config_path.name in CONFIG_ALLOWED_NAMES):
        print(
            'Failed: the configuration file must be named "cxxinit.yml" or "cxxinit.yaml".'
        )
        exit(1)

    if not config_path.exists():
        print("Failed: configuration file not found.")
        exit(2)

    proj = Project(args.config)

    if not treemaker.make_tree(proj, args.add):
        print(
            "Failed: directory is not empty. "
            "Use the -a option to add project files to an existing directory. "
            "Or manually delete the old version of the project."
        )
        exit(3)

    cmakegen.generate_lists(proj)
    _, not_found = fetcher.fetch_all(proj)

    for item in not_found:
        print(f'Note: not found "{item}".')

    print(f"The project has been successfully created ({proj.path}).")
    exit(0)
