from __future__ import annotations

from pathlib import Path

import click
from fastapi import APIRouter
from fastapi import status as http_status

from src.api.schemas import CourseResponse, SeedCoursesRequest, SeedCoursesResponse
from src.cli.loaders import load_courses
from src.services import list_courses, seed_courses

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/seed", response_model=SeedCoursesResponse)
def seed_courses_endpoint(
    payload: SeedCoursesRequest,
) -> SeedCoursesResponse:
    courses = load_courses(Path(payload.file_path))
    if not courses:
        raise click.ClickException("No courses found in the provided file.")

    created = seed_courses(courses)
    return SeedCoursesResponse(inserted=created)


@router.get("", response_model=list[CourseResponse], status_code=http_status.HTTP_200_OK)
def list_courses_endpoint() -> list[CourseResponse]:
    courses = list_courses()
    return [CourseResponse.model_validate(course) for course in courses]
