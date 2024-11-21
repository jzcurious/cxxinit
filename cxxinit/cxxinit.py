from cxxinit.model import Project
import cxxinit.treemaker as treemaker
import cxxinit.cmakegen as cmakegen
import cxxinit.fetcher as fetcher
import cxxinit.constansts as constansts
from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import argv


def parse_args() -> tuple[ArgumentParser, Namespace]:
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
        default=None,
        help="specify the path to the configuration file or existing project directory",
    )

    parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="add files to existing project",
    )

    return parser, parser.parse_args()


def print_sample():
    with constansts.SAMPLE_CONFIG_PATH.open("r") as f:
        print(f.read())


def find_config(passed_path: str | None) -> Path | None:
    config_path = Path(".") if not passed_path else Path(passed_path)

    if config_path.is_dir():
        for name in constansts.CONFIG_ALLOWED_NAMES:
            path = config_path.joinpath(name)
            if path.exists():
                return path

    if config_path.is_dir() or not config_path.exists():
        print("Failed: configuration file not found.")
        return None

    if not (config_path.name in constansts.CONFIG_ALLOWED_NAMES):
        print(
            'Failed: the configuration file must be named "cxxinit.yml" or "cxxinit.yaml".'
        )
        return None

    return config_path


def make_project(config_path: Path, add: bool = False) -> Project | None:
    proj = Project(config_path)

    if not treemaker.make_tree(proj, add):
        print(
            "Failed: directory is not empty. "
            "Use the -a option to add project files to an existing directory. "
            "Or manually delete the old version of the project."
        )
        return None

    cmakegen.generate_lists(proj)
    _, not_found = fetcher.fetch_all(proj)

    for item in not_found:
        print(f'Note: not found "{item}".')

    print(f"The project has been successfully created ({proj.path}).")
    return proj


def main():
    parser, args = parse_args()

    if args.sample:
        print_sample()
        exit(0)

    config_path = find_config(args.config)

    if not config_path:
        exit(1)

    if make_project(config_path, args.add):
        exit(0)
    else:
        exit(2)


if __name__ == "__main__":
    main()
