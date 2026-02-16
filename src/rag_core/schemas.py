from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class CourseLike(Protocol):
    id: int
    name: str
    description: str


@dataclass(slots=True, frozen=True)
class RetrievedCourse:
    course_id: int
    name: str
    description: str
    score: float


@dataclass(slots=True, frozen=True)
class CourseIndexingStats:
    courses_count: int
    chunks_count: int
    collection_recreated: bool


@dataclass(slots=True, frozen=True)
class RecommendationResult:
    recommendation_text: str
    retrieved_courses: list[RetrievedCourse]
    query_text: str
    prompt_text: str
    llm_response: Any
