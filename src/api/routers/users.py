from __future__ import annotations

from pathlib import Path

import click
from fastapi import APIRouter, status

from src.api.schemas import (
    CreateUserRequest,
    SeedUsersRequest,
    SeedUsersResponse,
    UserResponse,
)
from src.cli.loaders import load_users
from src.services import create_user, list_users, seed_users

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    payload: CreateUserRequest,
) -> UserResponse:
    user = create_user(
        login=payload.login,
        digital_footprints=payload.digital_footprints,
    )
    response: UserResponse = UserResponse.model_validate(user)
    return response


@router.get("", response_model=list[UserResponse])
def list_users_endpoint() -> list[UserResponse]:
    users = list_users()
    return [UserResponse.model_validate(user) for user in users]


@router.post("/seed", response_model=SeedUsersResponse)
def seed_users_endpoint(
    payload: SeedUsersRequest,
) -> SeedUsersResponse:
    users = load_users(Path(payload.file_path))
    if not users:
        raise click.ClickException("No users found in the provided file.")

    stats = seed_users(users)
    return SeedUsersResponse(created=stats.created, updated=stats.updated, skipped=stats.skipped)
