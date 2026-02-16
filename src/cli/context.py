from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CLIContext:
    database_url: str | None = None
    echo_sql: bool = False
