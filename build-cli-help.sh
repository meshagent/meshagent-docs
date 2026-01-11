#!/bin/bash

set -euo pipefail

OUTPUT_LOCATION=reference/meshagent_cli_help.mdx

echo "Generating the docs and saving to $OUTPUT_LOCATION"

MESHAGENT_CLI_BUILD=1 python3 -m typer meshagent.cli.cli utils docs --name meshagent \
  | sed 's/{/\&#123;/g; s/}/\&#125;/g' \
  > $OUTPUT_LOCATION

(
  printf '%s\n' '---' 'title: MeshAgent CLI Commands' '---' ''
  cat $OUTPUT_LOCATION
) > /tmp/$$.md && mv /tmp/$$.md $OUTPUT_LOCATION
