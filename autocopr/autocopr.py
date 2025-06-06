import logging
import subprocess
from pathlib import Path

import autocopr.cli
import autocopr.latestver
import autocopr.specdata
import autocopr.update
import yaml


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
    """
    Updates version information in all `.spec` files within a specified directory.

    Parses command-line arguments to determine the target directory, verbosity, and update options. Validates the environment for git operations if required. Recursively parses all `.spec` files, exits if any fail to parse, and retrieves the latest version information for each spec. If not in dry-run mode, updates spec files where newer versions are available, optionally performing in-place edits and git pushes. Prints a summary of version changes and provides instructions or status messages based on the chosen options.
    """
    args = autocopr.cli.create_parser().parse_args()
    root_dir = Path(args.directory)

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if (
        args.push
        and subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True
        ).returncode
        != 0
    ):
        # We're not in a git repository, exit
        logging.error("Cannot use --push when not running in a git repository")
        exit(1)

    # Load config file
    config = load_config("config.yaml")
    exclude_files = set(config.get("exclude_files", []))

    # Parse spec files, excluding those in exclude_files
    all_specs = root_dir.glob("**/*.spec")
    non_filtered_specs = [
        autocopr.specdata.parse_spec(spec)
        for spec in all_specs
        if spec.name not in exclude_files
    ]

    if None in non_filtered_specs:
        logging.warning("A spec/specs failed to parse, exiting...")
        exit(1)

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

    if not args.dry_run:
        for spec, latest in latest_vers:
            if spec.version != latest.ver:
                autocopr.update.update_version(
                    spec, latest, inplace=args.in_place, push=args.push
                )

    print("\n".join(update_summary))

    if args.dry_run:
        print("To update the spec files, run again without the dry-run flag.")
    elif not args.in_place:
        print(
            "If any specs were updated, the original spec files now have a "
            ".bk suffix, and the spec files are updated with the newest "
            "version."
        )
    else:
        print("Any updates have been applied to the spec files.")


if __name__ == "__main__":
    main()
