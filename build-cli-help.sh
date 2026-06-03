#!/bin/bash

set -euo pipefail

OUTPUT_LOCATION=reference/meshagent_cli_help.mdx
PYTHON_BIN=python3

if [ -n "${VIRTUAL_ENV:-}" ] && [ -x "$VIRTUAL_ENV/bin/python3" ]; then
  PYTHON_BIN="$VIRTUAL_ENV/bin/python3"
elif [ -n "${VIRTUAL_ENV:-}" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
  PYTHON_BIN="$VIRTUAL_ENV/bin/python"
elif [ -x ../meshagent-cli/.venv/bin/python3 ]; then
  PYTHON_BIN=../meshagent-cli/.venv/bin/python3
elif [ -x ../meshagent-cli/.venv/bin/python ]; then
  PYTHON_BIN=../meshagent-cli/.venv/bin/python
elif [ -x ../../.venv/bin/python3 ]; then
  PYTHON_BIN=../../.venv/bin/python3
elif [ -x ../../.venv/bin/python ]; then
  PYTHON_BIN=../../.venv/bin/python
elif command -v python3.13 >/dev/null 2>&1; then
  PYTHON_BIN=$(command -v python3.13)
fi

echo "Generating the docs and saving to $OUTPUT_LOCATION"

MESHAGENT_CLI_BUILD=1 "$PYTHON_BIN" build_cli_help.py
