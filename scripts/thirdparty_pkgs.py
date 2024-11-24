#!/bin/env python3

from collections import namedtuple

Git_package = namedtuple(
    "Git_package",
    ["name", "source_dict"],
)


def source_dict(
    clone_url=None,
    committish=None,
    subdirectory=None,
    specfile=None,
    source_build_method="rpkg",
):
    source_dict_pkg = dict(
        {
            "clone_url": clone_url,
            "committish": committish,
            "subdirectory": subdirectory,
            "spec": specfile,
            "scm_type": "git",
            "source_build_method": source_build_method,
        }
    )
    return source_dict_pkg


def thirdparty_packages_dict():
    thirdparty_packages = {
        "packages": [
            Git_package(
                "rust_tealdeer",
                source_dict(
                    clone_url="https://src.fedoraproject.org/rpms/rust-tealdeer",
                    specfile="rust-tealdeer.spec",
                ),
            )._asdict(),
            Git_package(
                "wezterm",
                source_dict(
                    clone_url="https://github.com/wez/wezterm.git",
                    source_build_method="make_srpm",
                ),
            )._asdict(),
            Git_package(
                "zed",
                source_dict(
                    clone_url="https://github.com/terrapkg/packages",
                    subdirectory="/anda/devs/zed/stable",
                    specfile="zed.spec",
                ),
            )._asdict(),
            Git_package(
                "zed-preview",
                source_dict(
                    clone_url="https://github.com/terrapkg/packages",
                    subdirectory="/anda/devs/zed/preview",
                    specfile="zed-preview.spec",
                ),
            )._asdict(),
        ]
    }
    # print(thirdparty_packages["packages"])
    # print(type(thirdparty_packages))
    # print(type(thirdparty_packages["packages"]))
    return thirdparty_packages


if __name__ == "__main__":
    thirdparty_packages_dict()  # This calls your main function
