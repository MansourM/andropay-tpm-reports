"""Tests for data models."""

import pytest
from src.models import Priority, Status


class TestPriorityEnum:
    """Tests for Priority enum."""

    def test_should_have_fire_priority(self):
        """P🔥 represents unplanned urgent work."""
        assert Priority.FIRE.value == "P🔥"

    def test_should_have_p0_priority(self):
        """P0 represents critical priority."""
        assert Priority.P0.value == "P0"

    def test_should_have_p1_priority(self):
        """P1 represents high priority."""
        assert Priority.P1.value == "P1"

    def test_should_have_p2_priority(self):
        """P2 represents medium priority."""
        assert Priority.P2.value == "P2"

    def test_should_create_from_string(self):
        """Should be able to create Priority from string value."""
        assert Priority("P🔥") == Priority.FIRE
        assert Priority("P0") == Priority.P0
        assert Priority("P1") == Priority.P1
        assert Priority("P2") == Priority.P2


class TestStatusEnum:
    """Tests for Status enum."""

    def test_should_have_backlog_status(self):
        """Backlog represents items not yet started."""
        assert Status.BACKLOG.value == "Backlog"

    def test_should_have_todo_status(self):
        """Todo represents items ready to start."""
        assert Status.TODO.value == "Todo"

    def test_should_have_pending_status(self):
        """Pending represents blocked items."""
        assert Status.PENDING.value == "Pending"

    def test_should_have_in_progress_status(self):
        """In Progress represents active work."""
        assert Status.IN_PROGRESS.value == "In Progress"

    def test_should_have_in_review_status(self):
        """In Review represents items under review."""
        assert Status.IN_REVIEW.value == "In Review"

    def test_should_have_done_status(self):
        """Done represents completed items."""
        assert Status.DONE.value == "Done"

    def test_should_create_from_string(self):
        """Should be able to create Status from string value."""
        assert Status("Backlog") == Status.BACKLOG
        assert Status("Todo") == Status.TODO
        assert Status("Pending") == Status.PENDING
        assert Status("In Progress") == Status.IN_PROGRESS
        assert Status("In Review") == Status.IN_REVIEW
        assert Status("Done") == Status.DONE



class TestProjectItem:
    """Tests for ProjectItem data class."""

    def test_should_create_project_item_with_all_fields(self):
        """Should create ProjectItem with all required fields."""
        from src.models import ProjectItem
        
        item = ProjectItem(
            id="PVTI_123",
            title="تسک تست",
            status=Status.TODO,
            priority=Priority.P1,
            assignees=["user1", "user2"],
            estimate_hours=5.0,
            labels=["bug", "urgent"],
            url="https://github.com/test/repo/issues/1",
            repository="test/repo",
            issue_number=1
        )
        
        assert item.id == "PVTI_123"
        assert item.title == "تسک تست"
        assert item.status == Status.TODO
        assert item.priority == Priority.P1
        assert item.assignees == ["user1", "user2"]
        assert item.estimate_hours == 5.0
        assert item.labels == ["bug", "urgent"]
        assert item.url == "https://github.com/test/repo/issues/1"
        assert item.repository == "test/repo"
        assert item.issue_number == 1

    def test_should_handle_optional_fields(self):
        """Should handle None values for optional fields."""
        from src.models import ProjectItem
        
        item = ProjectItem(
            id="PVTI_123",
            title="تسک تست",
            status=Status.TODO,
            priority=Priority.P1,
            assignees=[],
            estimate_hours=None,
            labels=[],
            url="https://github.com/test/repo/issues/1",
            repository="test/repo",
            issue_number=None
        )
        
        assert item.estimate_hours is None
        assert item.issue_number is None
        assert item.assignees == []
        assert item.labels == []

    def test_is_planned_should_return_true_for_planned_priorities(self):
        """Items with P0, P1, P2 should be considered planned."""
        from src.models import ProjectItem
        
        p0_item = ProjectItem(
            id="1", title="Test", status=Status.TODO, priority=Priority.P0,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        )
        p1_item = ProjectItem(
            id="2", title="Test", status=Status.TODO, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        )
        p2_item = ProjectItem(
            id="3", title="Test", status=Status.TODO, priority=Priority.P2,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        )
        
        assert p0_item.is_planned is True
        assert p1_item.is_planned is True
        assert p2_item.is_planned is True

    def test_is_planned_should_return_false_for_fire_priority(self):
        """Items with P🔥 should be considered unplanned."""
        from src.models import ProjectItem
        
        fire_item = ProjectItem(
            id="1", title="Test", status=Status.TODO, priority=Priority.FIRE,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        )
        
        assert fire_item.is_planned is False

    def test_is_active_should_return_true_for_non_done_items(self):
        """Items not in Done status should be considered active."""
        from src.models import ProjectItem
        
        backlog_item = ProjectItem(
            id="1", title="Test", status=Status.BACKLOG, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        )
        todo_item = ProjectItem(
            id="2", title="Test", status=Status.TODO, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        )
        in_progress_item = ProjectItem(
            id="3", title="Test", status=Status.IN_PROGRESS, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        )
        
        assert backlog_item.is_active is True
        assert todo_item.is_active is True
        assert in_progress_item.is_active is True

    def test_is_active_should_return_false_for_done_items(self):
        """Items in Done status should not be considered active."""
        from src.models import ProjectItem
        
        done_item = ProjectItem(
            id="1", title="Test", status=Status.DONE, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        )
        
        assert done_item.is_active is False



class TestProjectMetrics:
    """Tests for ProjectMetrics data class."""

    def test_should_create_project_metrics_with_all_fields(self):
        """Should create ProjectMetrics with all required fields."""
        from src.models import ProjectMetrics
        
        metrics = ProjectMetrics(
            total_items=76,
            total_estimate_hours=142.5,
            completion_percentage=26.3,
            planned_count=62,
            unplanned_count=14,
            unplanned_percentage=18.4,
            high_priority_not_started=5,
            items_by_status={"Todo": 14, "Done": 20},
            items_by_priority={"P1": 39, "P0": 14},
            items_by_assignee={"user1": 44, "user2": 4}
        )
        
        assert metrics.total_items == 76
        assert metrics.total_estimate_hours == 142.5
        assert metrics.completion_percentage == 26.3
        assert metrics.planned_count == 62
        assert metrics.unplanned_count == 14
        assert metrics.unplanned_percentage == 18.4
        assert metrics.high_priority_not_started == 5
        assert metrics.items_by_status == {"Todo": 14, "Done": 20}
        assert metrics.items_by_priority == {"P1": 39, "P0": 14}
        assert metrics.items_by_assignee == {"user1": 44, "user2": 4}

    def test_should_handle_zero_values(self):
        """Should handle zero values correctly."""
        from src.models import ProjectMetrics
        
        metrics = ProjectMetrics(
            total_items=0,
            total_estimate_hours=0.0,
            completion_percentage=0.0,
            planned_count=0,
            unplanned_count=0,
            unplanned_percentage=0.0,
            high_priority_not_started=0,
            items_by_status={},
            items_by_priority={},
            items_by_assignee={}
        )
        
        assert metrics.total_items == 0
        assert metrics.unplanned_percentage == 0.0
