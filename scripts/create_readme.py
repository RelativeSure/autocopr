#!/bin/env python3
import pathlib
from scripts.packages import packagelist

package_array = packagelist()

# Create markdown content for README.md
readme_content = """# Autocopr forked repo

## For any issues or questions related to python scripts, please go to upstream repo

<details open>

<summary>Status badges on COPR builds</summary>
"""

for name, url, version in package_array:
    readme_content += f"""
### {name} version {version}

![{name} status](https://copr.fedorainfracloud.org/coprs/relativesure/all-packages/package/{name}/status_image/last_build.png)
[Upstream]({url})
"""

# Example of how to convert markdown content to HTML (optional, for further use)
# html_content = markdown.markdown(markdown_content)

# Write markdown content to README.md
readme_path = pathlib.Path("README.md")
with readme_path.open("w", encoding="utf-8") as readme_file:
    readme_file.write(readme_content)

print("README.md file created successfully!")

# Example of how to use the html_content (optional)
# with open("README.html", "w", encoding="utf-8") as html_file:
#     html_file.write(html_content)
