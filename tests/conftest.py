"""Shared test fixtures for pytest."""

import pytest
from typing import List, Dict


@pytest.fixture
def sample_raw_item() -> Dict:
    """Provide a sample raw item from GitHub API."""
    return {
        "id": "PVTI_test123",
        "title": "نمونه تسک",
        "status": "Todo",
        "priority": "P1",
        "assignees": ["user1"],
        "estimate (Hrs)": 5.0,
        "labels": ["bug"],
        "content": {
            "url": "https://github.com/test/repo/issues/1",
            "repository": "test/repo",
            "number": 1
        }
    }


@pytest.fixture
def sample_raw_items() -> List[Dict]:
    """Provide multiple sample raw items."""
    return [
        {
            "id": "1",
            "title": "تسک اول",
            "status": "Todo",
            "priority": "P🔥",
            "assignees": ["user1"],
            "estimate (Hrs)": 3.0,
            "labels": ["urgent"],
            "content": {"url": "https://github.com/test/repo/issues/1"}
        },
        {
            "id": "2",
            "title": "تسک دوم",
            "status": "In Progress",
            "priority": "P1",
            "assignees": ["user2"],
            "estimate (Hrs)": 5.0,
            "labels": ["feature"],
            "content": {"url": "https://github.com/test/repo/issues/2"}
        },
        {
            "id": "3",
            "title": "تسک سوم",
            "status": "Done",
            "priority": "P1",
            "assignees": ["user1"],
            "estimate (Hrs)": 2.0,
            "labels": [],
            "content": {"url": "https://github.com/test/repo/issues/3"}
        }
    ]
