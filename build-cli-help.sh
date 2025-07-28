#!/bin/bash

set -euo pipefail

OUTPUT_LOCATION=reference/meshagent_cli_help.mdx
SKIP_INSTALL=
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip)
      SKIP_INSTALL=true
      shift
      ;;
    --install)
      SKIP_INSTALL=false
      shift
      ;;
    *)
      echo "Usage: $0 [--install | --skip]"
      exit 1
      ;;
  esac
done

if [ -z $SKIP_INSTALL ]; then
  echo "The meshagent-cli must be pip installed for typer to generate the docs."
  echo "Create a temporary venv and install the meshagent-cli packages from the meshagent-sdk folder?"
  echo "[1] Yes (use --install)"
  echo "[2] Skip the install and generate the docs. I know what I'm doing (use --skip)"
  echo "[3] Exit"
  read -r -p "Choose an option [1-3]: " REPLY
  case "$REPLY" in
    1)
      SKIP_INSTALL=false
      ;;
    2)
      SKIP_INSTALL=true
      ;;
    3)
      exit 0
      ;;
    *)
      echo "Invalid choice. Aborted."
      exit 1
      ;;
  esac
fi

if ! $SKIP_INSTALL; then
    # ensure cleanup on exit
    trap 'echo "Cleaning up..."; deactivate &>/dev/null || true; rm -rf temp-build-cli-help-venv' EXIT

    echo "Creating the venv..."
    python3 -m venv temp-build-cli-help-venv
    source temp-build-cli-help-venv/bin/activate

    echo "Installing the pips..."
    python3 -m pip install --upgrade pip
    pip install \
    -e "../meshagent-api[all]" \
    -e "../meshagent-agents[all]" \
    -e ../meshagent-tools \
    -e ../meshagent-openai \
    -e ../meshagent-otel \
    -e ../meshagent-mcp \
    -e ../meshagent-fal \
    -e ../meshagent-livekit \
    -e ../meshagent-perplexity \
    -e ../meshagent-firecrawl \
    -e ../meshagent-markitdown \
    -e ../meshagent-replicate \
    -e ../meshagent-computers \
    -e ../meshagent-cli
fi

echo "Generating the docs and saving to $OUTPUT_LOCATION"
# generate markdown with Typer
python3 -m typer meshagent.cli.cli utils docs --name meshagent > $OUTPUT_LOCATION

(
  printf '%s\n' '---' 'title: MeshAgent CLI Commands' '---' ''
  cat $OUTPUT_LOCATION
) > /tmp/$$.md && mv /tmp/$$.md $OUTPUT_LOCATION

#
#sed "${SED_BACKUP_OPTION[@]}" '1i\
#---\
#title: MeshAgent CLI Commands\
#---\
#' $OUTPUT_LOCATION