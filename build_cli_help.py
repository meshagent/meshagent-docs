from __future__ import annotations

import os
from pathlib import Path
from typing import Final

import click
from typer.cli import get_docs_for_click
from typer.core import MARKUP_MODE_KEY
from typer.main import get_command

os.environ.setdefault("MESHAGENT_CLI_BUILD", "1")

from meshagent.cli.cli import app as meshagent_app


OUTPUT_LOCATION: Final[Path] = Path("reference/meshagent_cli_help.mdx")
FRONT_MATTER: Final[str] = "---\ntitle: MeshAgent CLI Commands\n---\n\n"


def _top_level_hidden_group_names() -> set[str]:
    hidden_names: set[str] = set()
    for group in meshagent_app.registered_groups:
        if group.hidden is not True or group.name is None:
            continue
        hidden_names.add(group.name)
    return hidden_names


def _remove_hidden_root_bullets(docs: str, hidden_names: set[str]) -> str:
    lines = docs.splitlines()
    filtered_lines: list[str] = []
    reached_first_subsection = False

    for line in lines:
        if line.startswith("## "):
            reached_first_subsection = True

        if not reached_first_subsection and line.startswith("* `"):
            end_index = line.find("`", 3)
            if end_index != -1:
                command_name = line[3:end_index]
                if command_name in hidden_names:
                    continue

        filtered_lines.append(line)

    return "\n".join(filtered_lines)


def _remove_hidden_root_sections(docs: str, hidden_names: set[str]) -> str:
    hidden_headers = {f"## `meshagent {name}`" for name in hidden_names}
    lines = docs.splitlines()
    filtered_lines: list[str] = []
    skipping_hidden_section = False

    for line in lines:
        if line.startswith("## "):
            if line in hidden_headers:
                skipping_hidden_section = True
                continue
            skipping_hidden_section = False

        if skipping_hidden_section:
            continue

        filtered_lines.append(line)

    return "\n".join(filtered_lines)


def _strip_hidden_top_level_groups(docs: str) -> str:
    hidden_names = _top_level_hidden_group_names()
    docs_without_hidden_bullets = _remove_hidden_root_bullets(docs, hidden_names)
    return _remove_hidden_root_sections(docs_without_hidden_bullets, hidden_names)


def main() -> None:
    click_command = get_command(meshagent_app)
    ctx = click.Context(click_command)
    if meshagent_app.rich_markup_mode is not None:
        ctx.obj = {MARKUP_MODE_KEY: meshagent_app.rich_markup_mode}

    docs = get_docs_for_click(obj=click_command, ctx=ctx, name="meshagent").strip()
    docs = _strip_hidden_top_level_groups(docs)
    escaped_docs = docs.replace("{", "&#123;").replace("}", "&#125;")
    OUTPUT_LOCATION.write_text(f"{FRONT_MATTER}{escaped_docs}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
