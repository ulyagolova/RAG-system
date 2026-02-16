from __future__ import annotations

from collections.abc import Iterable, Sequence


def render_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    row_list = [list(map(str, headers))]
    row_list.extend([list(map(str, row)) for row in rows])
    if not row_list:
        return ""

    column_count = len(row_list[0])
    widths = [0] * column_count
    for row in row_list:
        for idx in range(column_count):
            widths[idx] = max(widths[idx], len(row[idx]))

    lines: list[str] = []
    header = " | ".join(row_list[0][idx].ljust(widths[idx]) for idx in range(column_count))
    separator = "-+-".join("-" * widths[idx] for idx in range(column_count))
    lines.append(header)
    lines.append(separator)

    for row in row_list[1:]:
        lines.append(" | ".join(row[idx].ljust(widths[idx]) for idx in range(column_count)))
    return "\n".join(lines)
