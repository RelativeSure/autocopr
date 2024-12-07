#!/bin/env python3
from thirdparty_pkgs import thirdparty_packages_dict
from copr.v3 import Client

thirdparty_pkgs_array = thirdparty_packages_dict()

# COPR API Client
client = Client.create_from_config_file()

list_copr_pkgs = client.package_proxy.get_list("relativesure", "all-packages")

for pkg in thirdparty_pkgs_array["packages"]:
    print(pkg["name"])
    print("hi")
