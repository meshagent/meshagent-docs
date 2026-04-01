#!/bin/bash

set -euo pipefail

OUTPUT_LOCATION=reference/meshagent_cli_help.mdx
PYTHON_BIN=python3

if [ -x ../../.venv/bin/python3 ]; then
  PYTHON_BIN=../../.venv/bin/python3
elif [ -x ../../.venv/bin/python ]; then
  PYTHON_BIN=../../.venv/bin/python
fi

echo "Generating the docs and saving to $OUTPUT_LOCATION"

MESHAGENT_CLI_BUILD=1 "$PYTHON_BIN" build_cli_help.py
