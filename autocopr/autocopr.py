import logging
import os
import subprocess
from pathlib import Path

import autocopr.cli
import autocopr.latestver
import autocopr.specdata
import autocopr.update
import yaml
from autocopr.cli import Mode


def load_config(config_file):
    """Loads the YAML config file and returns the content."""
    try:
        with open(config_file, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.warning(
            f"Config file {config_file} not found. Proceeding without exclusions."
        )
        return {}
    except yaml.YAMLError as e:
        logging.error(f"Error parsing the config file: {e}")
        exit(1)


def main():
    args = autocopr.cli.create_parser().parse_args()
    root_dir = Path(args.directory).absolute().resolve()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if not root_dir.is_dir():
        logging.error(
            f"Provided root directory {root_dir} is not a directory. "
            "Please provide a directory to start searching for spec files from. "
            "Exiting..."
        )
        exit(1)

    os.chdir(root_dir)

    if (
        args.mode == Mode.Push
        and subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True
        ).returncode
        != 0
    ):
        # We're not in a git repository, exit
        logging.error("Cannot use --push when not running in a git repository")
        exit(1)

    # Load config file for exclusions, in addition to the --ignore flag
    config = load_config("config.yaml")
    exclude_files = set(config.get("exclude_files", []))

    paths_to_ignore = set(root_dir / file for file in args.ignore)

    if args.ignore:
        logging.info(f"Ignoring {paths_to_ignore} due to --ignore flag")

    if exclude_files:
        logging.info(f"Excluding {exclude_files} due to config.yaml exclude_files")

    paths_to_parse = (
        path
        for path in root_dir.glob("**/*.spec")
        if path not in paths_to_ignore and path.name not in exclude_files
    )

    non_filtered_specs = [
        spec
        for spec_path in paths_to_parse
        if (spec := autocopr.specdata.parse_spec(spec_path)) is not None
    ]

    specs = [spec for spec in non_filtered_specs if spec is not None]

    latest_vers = autocopr.latestver.get_latest_versions(
        specs,
        root_dir / "graphql_id_cache.json",
        args.github_token,
        args.rest if args.rest else None,
    )

    update_summary = [f"{'Name':15}\t{'Old Version':8}\tNew Version"]

    update_summary += [
        f"{spec.name:15}\t{spec.version:8}\t"
        f"{'(no update)' if spec.version == latest.ver else latest.ver}"
        for (spec, latest) in latest_vers
    ]

    print("\n".join(update_summary))

    had_updates = [
        (spec, latest) for (spec, latest) in latest_vers if spec.version != latest.ver
    ]

    if len(had_updates) == 0:
        print("All spec files are up to date!")
        exit(0)

    match args.mode:
        case Mode.Update | Mode.Push:
            for spec, latest in had_updates:
                autocopr.update.update_version(
                    spec, latest, push=(args.mode == Mode.Push), verbose=args.verbose
                )

            if args.mode == Mode.Update:
                print(
                    "All spec files are now up to date. If updated, "
                    "the original spec file is backed up as a .bak file."
                )
            else:
                print(
                    "All spec files are now up to date, and the updates have been "
                    "pushed."
                )

        case Mode.DryRun | Mode.Check:
            print(
                f"{[spec.name for (spec, _) in had_updates]} "
                f"{'is' if len(had_updates) == 1 else 'are'} outdated."
            )
            if args.mode == Mode.Check:
                print("Exiting with an error because we are in check mode.")
                exit(1)


if __name__ == "__main__":
    main()
