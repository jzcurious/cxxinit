from cxxinit.model import Project
import cxxinit.treemaker as treemaker
import cxxinit.cmakegen as cmakegen
import cxxinit.fetcher as fetcher
import cxxinit.constansts as constansts
from argparse import ArgumentParser
from pathlib import Path
from sys import argv


def main():
    parser = ArgumentParser()

    parser.add_argument(
        "-s",
        "--sample",
        action="store_true",
        help="print sample configuration and exit",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=constansts.SAMPLE_CONFIG_PATH,
        help="specify the path to the configuration file",
    )

    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="add files to existing project",
    )

    if len(argv) == 1:
        parser.print_usage()
        exit(0)

    args = parser.parse_args()

    if args.sample:
        with constansts.SAMPLE_CONFIG_PATH.open("r") as f:
            print(f.read())
        exit(0)

    config_path = Path(args.config)

    if not (config_path.name in constansts.CONFIG_ALLOWED_NAMES):
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


if __name__ == "__main__":
    main()
