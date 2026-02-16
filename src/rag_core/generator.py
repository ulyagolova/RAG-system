from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from src.config.settings import AppSettings
from src.rag_core.pipeline import RAGPipeline, RecommendationResult


async def generate_course_recommendation(
    digital_footprints: Mapping[str, Any] | Sequence[Mapping[str, Any]] | str,
    *,
    settings: AppSettings | None = None,
    top_k: int = 5,
    search_k: int = 20,
) -> RecommendationResult:
    pipeline = RAGPipeline(settings=settings)
    return await pipeline.generate_recommendation(
        digital_footprints=digital_footprints,
        top_k=top_k,
        search_k=search_k,
    )
