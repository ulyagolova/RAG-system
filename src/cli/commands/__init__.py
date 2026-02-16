from __future__ import annotations

from src.cli.commands.courses import seed_courses_command, show_courses_command
from src.cli.commands.db import init_db_command
from src.cli.commands.recommendations import (
    add_recommendation_command,
    generate_recommendation_command,
    show_recommendations_command,
)
from src.cli.commands.users import create_user_command, seed_users_command, show_users_command

ALL_COMMANDS = (
    init_db_command,
    seed_courses_command,
    seed_users_command,
    create_user_command,
    add_recommendation_command,
    generate_recommendation_command,
    show_users_command,
    show_courses_command,
    show_recommendations_command,
)
