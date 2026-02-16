from __future__ import annotations

from fastapi import APIRouter, status

from src.api.schemas import (
    AddRecommendationRequest,
    GenerateRecommendationRequest,
    GenerateRecommendationResponse,
    RecommendationResponse,
    RetrievedCourseResponse,
)
from src.services import add_recommendation, generate_recommendation, list_recommendations

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("", response_model=RecommendationResponse, status_code=status.HTTP_201_CREATED)
def add_recommendation_endpoint(
    payload: AddRecommendationRequest,
) -> RecommendationResponse:
    recommendation = add_recommendation(
        login=payload.login,
        text=payload.text,
    )
    response: RecommendationResponse = RecommendationResponse.model_validate(recommendation)
    return response


@router.get("/{login}", response_model=list[RecommendationResponse], status_code=status.HTTP_200_OK)
def list_recommendations_endpoint(
    login: str,
) -> list[RecommendationResponse]:
    recommendations = list_recommendations(
        login=login,
    )
    return [RecommendationResponse.model_validate(item) for item in recommendations]


@router.post("/generate", response_model=GenerateRecommendationResponse, status_code=status.HTTP_201_CREATED)
def generate_recommendation_endpoint(
    payload: GenerateRecommendationRequest,
) -> GenerateRecommendationResponse:
    result = generate_recommendation(
        login=payload.login,
        top_k=payload.top_k,
        search_k=payload.search_k,
    )
    return GenerateRecommendationResponse(
        recommendation=RecommendationResponse.model_validate(result.recommendation),
        debug_file_path=str(result.debug_file_path),
        query_text=result.query_text,
        retrieved_courses=[
            RetrievedCourseResponse(
                course_id=item.course_id,
                name=item.name,
                description=item.description,
                score=item.score,
            )
            for item in result.retrieved_courses
        ],
    )
