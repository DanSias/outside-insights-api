from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Dict, Any
from app.models.prompt import Prompt
from app.models.response import Response
from app.models.user import User


class AnalyticsService:
    """Service for tracking and analyzing AI API usage."""

    @staticmethod
    def generate_usage_report(db: Session) -> List[Dict[str, Any]]:
        """
        Generate a report of user prompt activity.

        Args:
            db (Session): Database session.

        Returns:
            List[Dict[str, Any]]: List of users with their prompt and token usage.
        """
        results = (
            db.query(
                User.id.label("user_id"),
                User.email.label("email"),
                func.count(Prompt.id).label("prompt_count"),
                func.sum(Response.token_count).label("total_tokens_used"),
            )
            .join(Prompt, User.id == Prompt.user_id)
            .join(Response, Prompt.id == Response.prompt_id)
            .group_by(User.id, User.email)
            .all()
        )

        return [
            {
                "user_id": row.user_id,
                "email": row.email,
                "prompt_count": row.prompt_count,
                "total_tokens_used": row.total_tokens_used or 0,
            }
            for row in results
        ]

    @staticmethod
    def get_top_users_by_prompt_count(
        db: Session, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get the top users based on the number of prompts submitted.

        Args:
            db (Session): Database session.
            limit (int, optional): Number of top users to return. Defaults to 5.

        Returns:
            List[Dict[str, Any]]: List of users with their prompt count.
        """
        results = (
            db.query(
                User.id.label("user_id"),
                User.email.label("email"),
                func.count(Prompt.id).label("prompt_count"),
            )
            .join(Prompt, User.id == Prompt.user_id)
            .group_by(User.id, User.email)
            .order_by(func.count(Prompt.id).desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "user_id": row.user_id,
                "email": row.email,
                "prompt_count": row.prompt_count,
            }
            for row in results
        ]

    @staticmethod
    def get_token_usage_by_organization(db: Session) -> List[Dict[str, Any]]:
        """
        Get total LLM token usage for each organization.

        Args:
            db (Session): Database session.

        Returns:
            List[Dict[str, Any]]: List of organizations with token consumption.
        """
        results = (
            db.query(
                User.organization_id.label("organization_id"),
                func.count(Prompt.id).label("prompt_count"),
                func.sum(Response.token_count).label("total_tokens_used"),
            )
            .join(Prompt, User.id == Prompt.user_id)
            .join(Response, Prompt.id == Response.prompt_id)
            .group_by(User.organization_id)
            .all()
        )

        return [
            {
                "organization_id": row.organization_id,
                "prompt_count": row.prompt_count,
                "total_tokens_used": row.total_tokens_used or 0,
            }
            for row in results
        ]
