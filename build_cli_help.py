from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Final

import click
import typer
from typer.cli import get_docs_for_click
from typer.core import MARKUP_MODE_KEY

os.environ.setdefault("MESHAGENT_CLI_BUILD", "1")

from meshagent.cli.async_typer import LazyLoadedCommand, LazyTyper, get_command
from meshagent.cli.cli import app as meshagent_app


OUTPUT_LOCATION: Final[Path] = Path("reference/meshagent_cli_help.mdx")
FRONT_MATTER: Final[str] = "---\ntitle: MeshAgent CLI Commands\n---\n\n"


def _is_hidden(value: object) -> bool:
    return value is True


def _is_deprecated(value: object) -> bool:
    return value is True


def _load_command_if_needed(command: click.Command) -> click.Command:
    if isinstance(command, LazyLoadedCommand):
        return command._load_command()
    return command


def _load_registration_target(module: str, attribute: str) -> object:
    imported = importlib.import_module(module)
    return imported.__dict__[attribute]


def _resolve_child_source_app(target: object) -> typer.Typer | None:
    if isinstance(target, typer.Typer):
        return target
    return None


def _iter_visible_commands(
    click_command: click.Command,
    *,
    source_app: typer.Typer | None = None,
) -> list[tuple[str, click.Command, typer.Typer | None]]:
    click_command = _load_command_if_needed(click_command)
    if not hasattr(click_command, "commands"):
        return []

    commands: list[tuple[str, click.Command, typer.Typer | None]] = []
    seen_names: set[str] = set()

    if isinstance(source_app, LazyTyper):
        for registration in source_app.registered_lazy_commands:
            if registration.name in seen_names:
                continue
            if _is_hidden(registration.hidden) or _is_deprecated(registration.deprecated):
                continue
            child_click = click_command.commands.get(registration.name)
            if child_click is None:
                continue
            child_source = _resolve_child_source_app(
                _load_registration_target(registration.module, registration.attribute)
            )
            commands.append((registration.name, child_click, child_source))
            seen_names.add(registration.name)

    if isinstance(source_app, typer.Typer):
        for group in source_app.registered_groups:
            if group.name is None or group.name in seen_names:
                continue
            if _is_hidden(group.hidden) or _is_hidden(group.typer_instance.info.hidden):
                continue
            if _is_deprecated(group.deprecated) or _is_deprecated(
                group.typer_instance.info.deprecated
            ):
                continue
            child_click = click_command.commands.get(group.name)
            if child_click is None:
                continue
            commands.append((group.name, child_click, group.typer_instance))
            seen_names.add(group.name)

        for command_info in source_app.registered_commands:
            if command_info.name is None or command_info.name in seen_names:
                continue
            if _is_hidden(command_info.hidden) or _is_deprecated(command_info.deprecated):
                continue
            child_click = click_command.commands.get(command_info.name)
            if child_click is None:
                continue
            commands.append((command_info.name, child_click, None))
            seen_names.add(command_info.name)

    if source_app is not None:
        return commands

    for name, command in click_command.commands.items():
        if getattr(command, "hidden", False) or getattr(command, "deprecated", False):
            continue
        commands.append((name, command, None))
    return commands


def _build_commands_block(
    commands: list[tuple[str, click.Command, typer.Typer | None]],
) -> list[str]:
    lines = ["**Commands**:", ""]
    for name, command, _source_app in commands:
        help_text = _load_command_if_needed(command).get_short_help_str()
        if help_text:
            lines.append(f"* `{name}`: {help_text}")
        else:
            lines.append(f"* `{name}`")
    return lines


def _build_context(command: click.Command) -> click.Context:
    command = _load_command_if_needed(command)
    ctx = click.Context(command)
    if meshagent_app.rich_markup_mode is not None:
        ctx.obj = {MARKUP_MODE_KEY: meshagent_app.rich_markup_mode}
    return ctx


def _render_command_docs(
    *,
    command: click.Command,
    command_name: str,
) -> str:
    command = _load_command_if_needed(command)
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
    commands: list[tuple[str, click.Command, typer.Typer | None]],
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
    source_app: typer.Typer | None = None,
) -> list[str]:
    command = _load_command_if_needed(command)
    commands = _iter_visible_commands(command, source_app=source_app)
    lines = _render_command_body(command=command, command_name=command_name)
    lines = _replace_commands_block(lines=lines, commands=commands)
    lines = _set_heading_level(lines=lines, depth=depth)

    sections = ["\n".join(lines).strip()]
    for child_name, child_command, child_source_app in commands:
        sections.extend(
            _render_recursive_sections(
                command=child_command,
                command_name=f"{command_name} {child_name}",
                depth=depth + 1,
                source_app=child_source_app,
            )
        )
    return sections


def main() -> None:
    click_command = get_command(meshagent_app)
    sections = _render_recursive_sections(
        command=click_command,
        command_name="meshagent",
        depth=0,
        source_app=meshagent_app,
    )
    docs = "\n\n".join(section for section in sections if section)
    escaped_docs = docs.replace("{", "&#123;").replace("}", "&#125;")
    OUTPUT_LOCATION.write_text(f"{FRONT_MATTER}{escaped_docs}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
