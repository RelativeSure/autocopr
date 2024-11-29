#!/bin/env python3

from collections import namedtuple

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

if __name__ == "__main__":
    thirdparty_packages_dict()
