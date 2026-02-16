from __future__ import annotations

import click

from src.cli.context import CLIContext
from src.cli.output import render_table
from src.services import (
    NotFoundError,
    ServiceError,
    add_recommendation,
    generate_recommendation,
    list_recommendations,
)


@click.command("add-recommendation")
@click.option("--login", required=True)
@click.option("--text", required=True)
@click.pass_obj
def add_recommendation_command(context: CLIContext, login: str, text: str) -> None:
    try:
        recommendation = add_recommendation(
            login=login,
            text=text,
            database_url=context.database_url,
            echo_sql=context.echo_sql,
        )
    except NotFoundError as exc:
        raise click.ClickException(str(exc)) from exc
    except ServiceError as exc:
        raise click.ClickException(str(exc)) from exc
    except Exception as exc:  # pragma: no cover - surfacing database errors to CLI
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Recommendation created with id={recommendation.id}.")


@click.command("show-recommendations")
@click.option("--login", required=True)
@click.pass_obj
def show_recommendations_command(context: CLIContext, login: str) -> None:
    try:
        recommendations = list_recommendations(
            login=login,
            database_url=context.database_url,
            echo_sql=context.echo_sql,
        )
    except NotFoundError as exc:
        raise click.ClickException(str(exc)) from exc
    except ServiceError as exc:
        raise click.ClickException(str(exc)) from exc
    except Exception as exc:  # pragma: no cover - surfacing database errors to CLI
        raise click.ClickException(str(exc)) from exc

    if not recommendations:
        click.echo("No recommendations found.")
        return

    rows = [[str(rec.id), rec.text, str(rec.created_at)] for rec in recommendations]
    click.echo(render_table(["ID", "Text", "Created At"], rows))


@click.command("generate_recommendation")
@click.option("--login", required=True)
@click.option("--top-k", default=5, show_default=True, type=click.IntRange(1, 20))
@click.option("--search-k", default=20, show_default=True, type=click.IntRange(1, 100))
@click.pass_obj
def generate_recommendation_command(
    context: CLIContext,
    login: str,
    top_k: int,
    search_k: int,
) -> None:
    try:
        result = generate_recommendation(
            login=login,
            top_k=top_k,
            search_k=search_k,
            database_url=context.database_url,
            echo_sql=context.echo_sql,
        )
    except NotFoundError as exc:
        raise click.ClickException(str(exc)) from exc
    except ServiceError as exc:
        raise click.ClickException(str(exc)) from exc
    except Exception as exc:  # pragma: no cover - surfacing runtime errors to CLI
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Recommendation generated with id={result.recommendation.id}.")
    click.echo(f"Debug trace saved to: {result.debug_file_path}")
    click.echo("Text:")
    click.echo(result.recommendation.text)
    click.echo("")
    click.echo("Retrieved similar courses:")
    if not result.retrieved_courses:
        click.echo("No similar courses were found in Qdrant.")
        return

    rows = [
        [
            str(course.course_id),
            course.name,
            f"{course.score:.3f}",
        ]
        for course in result.retrieved_courses
    ]
    click.echo(render_table(["Course ID", "Name", "Score"], rows))
