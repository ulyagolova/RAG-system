from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from src.config.settings import AppSettings, get_settings
from src.rag_core.embeddings import normalize_vector_size
from src.rag_core.indexer import index_courses_in_vector_db
from src.rag_core.llm import extract_llm_text, generate_llm_response
from src.rag_core.prompt_builder import format_courses_context, render_prompt
from src.rag_core.retriever import retrieve_courses_for_footprints
from src.rag_core.schemas import (
    CourseIndexingStats,
    CourseLike,
    RecommendationResult,
    RetrievedCourse,
)


class RAGPipeline:
    def __init__(
        self,
        *,
        settings: AppSettings | None = None,
        prompt_path: Path | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._prompt_path = (
            prompt_path or Path(__file__).resolve().parents[1] / "prompts" / "recommendation_prompt.txt"
        )

    async def index_courses(
        self,
        courses: Sequence[CourseLike],
        *,
        recreate_collection: bool = False,
    ) -> CourseIndexingStats:
        return await index_courses_in_vector_db(
            courses=courses,
            settings=self._settings,
            recreate_collection=recreate_collection,
        )

    async def retrieve_courses(
        self,
        digital_footprints: Mapping[str, Any] | Sequence[Mapping[str, Any]] | str,
        *,
        top_k: int = 5,
        search_k: int = 20,
    ) -> tuple[list[RetrievedCourse], str]:
        return await retrieve_courses_for_footprints(
            digital_footprints=digital_footprints,
            settings=self._settings,
            top_k=top_k,
            search_k=search_k,
        )

    async def generate_recommendation(
        self,
        digital_footprints: Mapping[str, Any] | Sequence[Mapping[str, Any]] | str,
        *,
        top_k: int = 5,
        search_k: int = 20,
    ) -> RecommendationResult:
        retrieved_courses, query_text = await self.retrieve_courses(
            digital_footprints=digital_footprints,
            top_k=top_k,
            search_k=search_k,
        )
        courses_context = format_courses_context(retrieved_courses)
        prompt = render_prompt(
            prompt_path=self._prompt_path,
            courses_context=courses_context,
            user_query=query_text,
        )
        recommendation_text, response_payload = await generate_llm_response(
            settings=self._settings,
            prompt=prompt,
        )
        return RecommendationResult(
            recommendation_text=recommendation_text,
            retrieved_courses=retrieved_courses,
            query_text=query_text,
            prompt_text=prompt,
            llm_response=response_payload,
        )

    # Kept for backward compatibility with existing tests and call sites.
    def _normalize_vector_size(self, vector: Sequence[float]) -> list[float]:
        return normalize_vector_size(vector, self._settings.embedding_vector_size)

    # Kept for backward compatibility with existing tests and call sites.
    def _render_prompt(self, *, courses_context: str, user_query: str) -> str:
        return render_prompt(
            prompt_path=self._prompt_path,
            courses_context=courses_context,
            user_query=user_query,
        )

    @staticmethod
    def _extract_llm_text(payload: Any) -> str:
        return extract_llm_text(payload)
