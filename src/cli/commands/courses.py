from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click

from src.cli.context import CLIContext
from src.cli.output import render_table
from src.services import ServiceError, ValidationError, list_courses, seed_courses


def _load_courses(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise click.ClickException(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"Invalid JSON in {path}: {exc}") from exc

    if isinstance(payload, list):
        return [course for course in payload if isinstance(course, dict)]
    if isinstance(payload, dict):
        courses = payload.get("courses")
        if isinstance(courses, list):
            return [course for course in courses if isinstance(course, dict)]
    raise click.ClickException("Courses JSON must be a list or an object with a 'courses' list.")


@click.command("seed-courses")
@click.option("--file", "file_path", type=click.Path(path_type=Path), required=True)
@click.pass_obj
def seed_courses_command(context: CLIContext, file_path: Path) -> None:
    courses = _load_courses(file_path)
    if not courses:
        raise click.ClickException("No courses found in the provided file.")

    try:
        created = seed_courses(
            courses,
            database_url=context.database_url,
            echo_sql=context.echo_sql,
        )
    except ValidationError as exc:
        raise click.ClickException(str(exc)) from exc
    except ServiceError as exc:
        raise click.ClickException(str(exc)) from exc
    except Exception as exc:  # pragma: no cover - surfacing database errors to CLI
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Inserted {created} new course(s).")


@click.command("show-courses")
@click.pass_obj
def show_courses_command(context: CLIContext) -> None:
    try:
        courses = list_courses(
            database_url=context.database_url,
            echo_sql=context.echo_sql,
        )
    except ServiceError as exc:
        raise click.ClickException(str(exc)) from exc
    except Exception as exc:  # pragma: no cover - surfacing database errors to CLI
        raise click.ClickException(str(exc)) from exc

    if not courses:
        click.echo("No courses found.")
        return

    rows = [[str(course.id), course.name, course.description] for course in courses]
    click.echo(render_table(["ID", "Name", "Description"], rows))
