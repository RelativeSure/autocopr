#!/bin/env python3
import pathlib

def packagelist():
    # Specify the directory path
    dir_path = pathlib.Path(".")

    # Use glob to retrieve a list of files
    files = dir_path.glob("specs/**/*.spec")  # only match .spec files

    # Sort the files by filename (natural sort)
    sorted_files = sorted(files, key=lambda x: x.name)

    # Array to store the name and URL pairs
    name_url_pairs = []

    # Process files and extract Name and URL
    for file in sorted_files:
        print(file)
        name = None
        url = None
        version = None
        with file.open("r", encoding="utf-8") as spec_file:
            for line in spec_file:
                if line.startswith("Name:"):
                    name = line.split(":", 1)[1].strip()
                elif line.startswith("URL:"):
                    url = line.split(":", 1)[1].strip()
                elif line.startswith("Version:"):
                    version = line.split(":", 1)[1].strip()
                # Break the loop if both Name, URL and version are found
                if name and url and version:
                    break
        if name and url and version:
            name_url_pairs.append((name, url, version))
            print(
                f"Processed: {file.name} -> Name: {name}, Version: {version}, URL: {url}"
            )
    return name_url_pairs


if __name__ == "__main__":
    packagelist()  # This calls your main function
