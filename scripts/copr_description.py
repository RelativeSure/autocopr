#!/bin/env python3
from copr.v3 import Client

# COPR API Client
client = Client.create_from_config_file()

# Import package list
from packages import packagelist
package_array = packagelist()

# Description
readme_content = "### List of packages"

for name, url, version in package_array:
    readme_content += f"""
`{name}` ( [Upstream]({url}) )
"""

# Instructions
instructions_content = """### Enable COPR repo
$`sudo dnf copr enable relativesure/python-test`


### Install all packages
$`sudo dnf install"""
for name, url, version in package_array:
    instructions_content += f" {name}"

instructions_content += "`"

# Setup copr repo
client.project_proxy.edit(
    "relativesure", # ownername
    "python-test", # projectname
    ['fedora-40-x86_64', 'fedora-41-x86_64', 'fedora-rawhide-x86_64'], # chroots
    description=readme_content,
    instructions=instructions_content,
    homepage="https://github.com/RelativeSure/autocopr",
    additional_repos="https://repos.fyralabs.com/terra$releasever/",
    unlisted_on_hp=True,
    enable_net=True,
    follow_fedora_branching=True
)
