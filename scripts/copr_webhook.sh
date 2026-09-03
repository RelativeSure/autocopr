#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <copr webhook url> <github sha>"
	exit 1
fi

COPR_WEBHOOK=$1
GITHUB_SHA=$2

# config.yaml's exclude_files list is a simple YAML block:
#   exclude_files:
#     - foo.spec
#     - bar.spec
# Read it without a YAML parser dependency: grab lines after the
# "exclude_files:" key that start with "- ", up to the next non-list line.
excluded_files=$(awk '/^exclude_files:/{f=1;next} f && /^[[:space:]]*-/{gsub(/^[[:space:]]*-[[:space:]]*/,"");print;next} f{exit}' config.yaml)
if [ -n "$excluded_files" ]; then
	echo "Excluded from COPR builds (config.yaml exclude_files): $excluded_files"
fi

files_changed=$(git diff-tree --no-commit-id --name-only -r "$GITHUB_SHA" | grep '\.spec$')
echo "Files changed: $files_changed"

for file in $files_changed; do
	echo "Processing file: $file"
	filename=$(basename "$file")

	if grep -qxF "$filename" <<<"$excluded_files"; then
		echo "Skipping $filename: excluded via config.yaml exclude_files"
		continue
	fi

	filename_without_ext="${filename%.*}"
	echo "Cleaned up $filename_without_ext by removing extension and specs folder"
	echo "Sending copr webhook of package $filename_without_ext"
	curl -X POST "$COPR_WEBHOOK/$filename_without_ext/"
done
