from __future__ import annotations

import click

from src.cli.commands import ALL_COMMANDS
from src.cli.context import CLIContext
from src.config.settings import get_settings
from src.utils import configure_logging


@click.group()
@click.pass_context
def cli(context: click.Context) -> None:
    configure_logging(get_settings().log_level)
    context.obj = CLIContext()


for command in ALL_COMMANDS:
    cli.add_command(command)
