#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <copr webhook url>"
  exit 1
fi

thirdparty_pkgs_array=(act-cli ghostty python-neovim rust-tealdeer utf8proc wezterm zed zed-preview)

for file in "${thirdparty_pkgs_array[@]}"; do
  echo "Processing file: $file"
  curl -i -H "Accept: application/json" -H "Content-Type:application/json" -X POST "$COPR_WEBHOOK/$file/"
done
