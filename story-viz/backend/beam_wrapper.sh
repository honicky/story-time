#!/bin/bash

GIT_BASE_DIR=$(git rev-parse --show-toplevel)

if [ ! -d "$GIT_BASE_DIR/lib" ]; then
    echo "Error: $GIT_BASE_DIR/lib directory does not exist" > /dev/stderr
    exit 1
fi

# The directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Create a tar archive of the lib directory and pipe it directly into tar for extraction in the script directory
tar -C "$GIT_BASE_DIR" -cf - lib | tar -xf - -C "$SCRIPT_DIR"

/usr/local/bin/beam "$@"
