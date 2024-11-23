#!/bin/env python3
from copr.v3 import Client

# COPR API Client
client = Client.create_from_config_file()

# Import package list
from packages import packagelist
package_array = packagelist()
thirdparty_package_array = ['rust-tealdeer', 'wezterm', 'zed', 'zed-preview']

# Description
readme_content = """
This COPR repo is for personal and work use.

Please go ahead and use this copr repo, be aware that the repo might be abandoned at any point.

Feel free to create a GitHub issue if there's any issues with the packages.

The following packages are installed from a 3rd party source than autocopr github repo.
```
"""

for thirdparty_package in thirdparty_package_array:
    readme_content += f"* {thirdparty_package}\n"

readme_content += """
```
### **List of packages from relativesure/autocopr github repos**
"""

for name, url, version in package_array:
    readme_content += f"""
`{name}` ( [Upstream]({url}) )
"""

# Instructions
instructions_content = """### **Enable COPR repo**
$`sudo dnf copr enable relativesure/all-packages`


### **Install all packages**
$`sudo dnf install"""
for name, url, version in package_array:
    instructions_content += f" {name}"

for thirdparty_package in thirdparty_package_array:
    instructions_content += f" {thirdparty_package}"

instructions_content += "`"

# Setup copr repo
client.project_proxy.edit(
    "relativesure", # ownername
    "all-packages", # projectname
    ['fedora-40-x86_64', 'fedora-41-x86_64', 'fedora-rawhide-x86_64'], # chroots
    description=readme_content,
    instructions=instructions_content,
    homepage="https://github.com/RelativeSure/autocopr",
    additional_repos="https://repos.fyralabs.com/terra$releasever/",
    unlisted_on_hp=False,
    enable_net=True,
    follow_fedora_branching=True
)
