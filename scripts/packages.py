#!/bin/env python3
import pathlib
from collections import namedtuple

def packagelist():
    # Specify the directory path
    dir_path = pathlib.Path(".")

    # Use glob to retrieve a list of files
    files = dir_path.glob("specs/*.spec")  # only match .spec files

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
    packagelist()

# ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
# │                                                                                                  │
# │  mmmm             #                                m                         #                   │
# │ "   "#  m mm   mmm#         mmmm    mmm    m mm  mm#mm  m   m         mmmm   #   m   mmmm   mmm  │
# │   mmm"  #"  " #" "#         #" "#  "   #   #"  "   #    "m m"         #" "#  # m"   #" "#  #   " │
# │     "#  #     #   #         #   #  m"""#   #       #     #m#          #   #  #"#    #   #   """m │
# │ "mmm#"  #     "#m##         ##m#"  "mm"#   #       "mm   "#           ##m#"  #  "m  "#m"#  "mmm" │
# │                             #                            m"           #              m  #        │
# │                             "                           ""            "               ""         │
# └──────────────────────────────────────────────────────────────────────────────────────────────────┘

Git_package = namedtuple("Git_package", ["name", "source_dict"])

def source_dict(clone_url=None, committish=None, subdirectory=None, specfile=None, source_build_method="rpkg"):
    return {
        "clone_url": clone_url,
        "committish": committish,
        "subdirectory": subdirectory,
        "spec": specfile,
        "scm_type": "git",
        "source_build_method": source_build_method,
    }

def create_git_package(name, clone_url, specfile=None, subdirectory=None, source_build_method="rpkg"):
    return Git_package(
        name,
        source_dict(
            clone_url=clone_url,
            specfile=specfile,
            subdirectory=subdirectory,
            source_build_method=source_build_method
        )
    )._asdict()

def thirdparty_packages_dict():
    package_definitions = [
        ("rust_tealdeer", "https://src.fedoraproject.org/rpms/rust-tealdeer", "rust-tealdeer.spec"),
        ("wezterm", "https://github.com/wez/wezterm.git", None, None, "make_srpm"),
        ("zed", "https://github.com/terrapkg/packages", "zed.spec", "/anda/devs/zed/stable"),
        ("zed-preview", "https://github.com/terrapkg/packages", "zed-preview.spec", "/anda/devs/zed/preview")
    ]
    
    thirdparty_packages = {
        "packages": [create_git_package(*pkg) for pkg in package_definitions]
    }

    return thirdparty_packages
