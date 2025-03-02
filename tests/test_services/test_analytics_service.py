import pytest
from unittest.mock import MagicMock
from app.services.analytics_service import AnalyticsService


@pytest.fixture
def mock_db():
    """Mock database session."""
    return MagicMock()


def test_generate_usage_report(mock_db):
    """Test generating an analytics usage report."""
    mock_db.query().all.return_value = [
        {"user_id": 1, "prompt_count": 10},
        {"user_id": 2, "prompt_count": 5},
    ]

    report = AnalyticsService.generate_usage_report(mock_db)
    assert len(report) == 2
    assert report[0]["user_id"] == 1
    assert report[1]["prompt_count"] == 5
