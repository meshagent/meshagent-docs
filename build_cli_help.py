from __future__ import annotations

import os
from pathlib import Path
from typing import Final

import click
from typer.cli import get_docs_for_click
from typer.core import MARKUP_MODE_KEY

os.environ.setdefault("MESHAGENT_CLI_BUILD", "1")

from meshagent.cli.async_typer import LazyTyper, get_command
from meshagent.cli.cli import app as meshagent_app


OUTPUT_LOCATION: Final[Path] = Path("reference/meshagent_cli_help.mdx")
FRONT_MATTER: Final[str] = "---\ntitle: MeshAgent CLI Commands\n---\n\n"


def _top_level_hidden_group_names() -> set[str]:
    hidden_names: set[str] = set()
    if isinstance(meshagent_app, LazyTyper):
        for registration in meshagent_app.registered_lazy_commands:
            if registration.hidden:
                hidden_names.add(registration.name)
    for group in meshagent_app.registered_groups:
        if group.hidden is not True or group.name is None:
            continue
        hidden_names.add(group.name)
    return hidden_names


def _iter_visible_commands(
    click_command: click.Command,
    *,
    hidden_names: set[str] | None = None,
) -> list[tuple[str, click.Command]]:
    if not hasattr(click_command, "commands"):
        return []

    commands: list[tuple[str, click.Command]] = []
    for name, command in click_command.commands.items():
        if hidden_names is not None and name in hidden_names:
            continue
        if hidden_names is None and getattr(command, "hidden", False):
            continue
        commands.append((name, command))
    return commands


def _build_commands_block(commands: list[tuple[str, click.Command]]) -> list[str]:
    lines = ["**Commands**:", ""]
    for name, command in commands:
        help_text = command.get_short_help_str()
        if help_text:
            lines.append(f"* `{name}`: {help_text}")
        else:
            lines.append(f"* `{name}`")
    return lines


def _build_context(command: click.Command) -> click.Context:
    ctx = click.Context(command)
    if meshagent_app.rich_markup_mode is not None:
        ctx.obj = {MARKUP_MODE_KEY: meshagent_app.rich_markup_mode}
    return ctx


def _render_command_docs(
    *,
    command: click.Command,
    command_name: str,
) -> str:
    ctx = _build_context(command)
    return get_docs_for_click(obj=command, ctx=ctx, name=command_name).strip()


def _render_command_body(
    *,
    command: click.Command,
    command_name: str,
) -> list[str]:
    docs = _render_command_docs(command=command, command_name=command_name)
    body_lines: list[str] = []
    for line in docs.splitlines():
        if line.startswith("## "):
            break
        body_lines.append(line)
    return body_lines


def _replace_commands_block(
    *,
    lines: list[str],
    commands: list[tuple[str, click.Command]],
) -> list[str]:
    replaced_lines: list[str] = []
    in_commands_block = False
    saw_commands_block = False

    for line in lines:
        if line == "**Commands**:":
            saw_commands_block = True
            in_commands_block = True
            continue
        if in_commands_block and line.startswith("* `"):
            continue
        if in_commands_block and line == "":
            continue
        replaced_lines.append(line)

    while replaced_lines and replaced_lines[-1] == "":
        replaced_lines.pop()

    if not saw_commands_block and len(commands) == 0:
        return replaced_lines
    return replaced_lines + [""] + _build_commands_block(commands)


def _set_heading_level(*, lines: list[str], depth: int) -> list[str]:
    if len(lines) == 0:
        return lines
    if not lines[0].startswith("# "):
        return lines
    lines[0] = f"{'#' * (depth + 1)} {lines[0][2:]}"
    return lines


def _render_recursive_sections(
    *,
    command: click.Command,
    command_name: str,
    depth: int,
    hidden_names: set[str] | None = None,
) -> list[str]:
    commands = _iter_visible_commands(command, hidden_names=hidden_names)
    lines = _render_command_body(command=command, command_name=command_name)
    lines = _replace_commands_block(lines=lines, commands=commands)
    lines = _set_heading_level(lines=lines, depth=depth)

    sections = ["\n".join(lines).strip()]
    for child_name, child_command in commands:
        sections.extend(
            _render_recursive_sections(
                command=child_command,
                command_name=f"{command_name} {child_name}",
                depth=depth + 1,
            )
        )
    return sections


def main() -> None:
    click_command = get_command(meshagent_app, materialize_lazy=True)
    sections = _render_recursive_sections(
        command=click_command,
        command_name="meshagent",
        depth=0,
        hidden_names=_top_level_hidden_group_names(),
    )
    docs = "\n\n".join(section for section in sections if section)
    escaped_docs = docs.replace("{", "&#123;").replace("}", "&#125;")
    OUTPUT_LOCATION.write_text(f"{FRONT_MATTER}{escaped_docs}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
