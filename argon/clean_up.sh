#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

shopt -s nullglob
for file in ./*; do
    name="${file##*/}"
    if [[ "$name" == \#*\# ]]; then
        rm -f -- "$file"
    fi
done

echo "Temporary GROMACS files starting and ending with '#' removed."
