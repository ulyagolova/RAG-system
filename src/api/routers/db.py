from __future__ import annotations

from pathlib import Path

import click
from fastapi import APIRouter

from src.api.schemas import InitDbRequest, InitDbResponse
from src.cli.loaders import load_courses
from src.services import init_db, list_and_vectorize_courses, seed_courses

router = APIRouter(prefix="/db", tags=["db"])


@router.post("/init", response_model=InitDbResponse)
def init_db_endpoint(
    payload: InitDbRequest,
) -> InitDbResponse:
    init_db(
        drop_existing=payload.drop_existing,
    )

    inserted = 0
    if not payload.skip_courses_seed:
        courses = load_courses(Path(payload.courses_file))
        if not courses:
            raise click.ClickException("No courses found in the provided file.")
        inserted = seed_courses(courses)

    stats = list_and_vectorize_courses(
        recreate_collection=payload.drop_existing,
    )
    return InitDbResponse(
        courses_seeded=inserted,
        courses_count=stats.courses_count,
        chunks_count=stats.chunks_count,
        collection_recreated=stats.collection_recreated,
    )
