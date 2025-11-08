"""Tests for data processor."""

import pytest
from src.models import Priority, Status, ProjectItem


class TestDataParsing:
    """Tests for parsing raw JSON to ProjectItem objects."""

    def test_should_parse_raw_item_to_project_item(self, sample_raw_item):
        """Should convert raw JSON item to ProjectItem object."""
        from src.processor import parse_item
        
        result = parse_item(sample_raw_item)
        
        assert isinstance(result, ProjectItem)
        assert result.id == "PVTI_test123"
        assert result.title == "نمونه تسک"
        assert result.status == Status.TODO
        assert result.priority == Priority.P1
        assert result.assignees == ["user1"]
        assert result.estimate_hours == 5.0
        assert result.labels == ["bug"]
        assert result.url == "https://github.com/test/repo/issues/1"

    def test_should_handle_missing_estimate_hours(self):
        """Should handle None for missing estimate hours."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "Todo",
            "priority": "P1",
            "assignees": [],
            "estimate (Hrs)": None,
            "labels": [],
            "content": {"url": "https://github.com/test/repo/issues/1"}
        }
        
        result = parse_item(raw_item)
        
        assert result.estimate_hours is None

    def test_should_handle_missing_assignees(self):
        """Should handle empty assignees list."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "Todo",
            "priority": "P1",
            "assignees": [],
            "estimate (Hrs)": 5.0,
            "labels": [],
            "content": {"url": "https://github.com/test/repo/issues/1"}
        }
        
        result = parse_item(raw_item)
        
        assert result.assignees == []

    def test_should_parse_fire_priority(self):
        """Should correctly parse P🔥 priority."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Urgent",
            "status": "In Progress",
            "priority": "P🔥",
            "assignees": ["user1"],
            "estimate (Hrs)": 3.0,
            "labels": ["urgent"],
            "content": {"url": "https://github.com/test/repo/issues/1"}
        }
        
        result = parse_item(raw_item)
        
        assert result.priority == Priority.FIRE
        assert result.is_planned is False

    def test_should_parse_multiple_items(self, sample_raw_items):
        """Should parse list of raw items."""
        from src.processor import parse_items
        
        results = parse_items(sample_raw_items)
        
        assert len(results) == 3
        assert all(isinstance(item, ProjectItem) for item in results)
        assert results[0].priority == Priority.FIRE
        assert results[1].status == Status.IN_PROGRESS
        assert results[2].status == Status.DONE

    def test_should_extract_repository_from_content(self):
        """Should extract repository info from content field."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "Todo",
            "priority": "P1",
            "assignees": [],
            "estimate (Hrs)": None,
            "labels": [],
            "content": {
                "url": "https://github.com/test/repo/issues/1",
                "repository": "test/repo",
                "number": 1
            }
        }
        
        result = parse_item(raw_item)
        
        assert result.repository == "test/repo"
        assert result.issue_number == 1

    def test_should_handle_missing_content_fields(self):
        """Should handle missing repository and issue_number."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "Todo",
            "priority": "P1",
            "assignees": [],
            "estimate (Hrs)": None,
            "labels": [],
            "content": {"url": "https://github.com/test/repo/issues/1"}
        }
        
        result = parse_item(raw_item)
        
        assert result.repository == ""
        assert result.issue_number is None



class TestMetricsCalculation:
    """Tests for metrics calculation."""

    def test_should_calculate_total_items(self, sample_raw_items):
        """Should count total number of items."""
        from src.processor import parse_items, calculate_metrics
        
        items = parse_items(sample_raw_items)
        metrics = calculate_metrics(items)
        
        assert metrics.total_items == 3

    def test_should_calculate_total_estimate_hours(self, sample_raw_items):
        """Should sum all estimate hours."""
        from src.processor import parse_items, calculate_metrics
        
        items = parse_items(sample_raw_items)
        metrics = calculate_metrics(items)
        
        assert metrics.total_estimate_hours == 10.0  # 3 + 5 + 2

    def test_should_calculate_completion_percentage(self, sample_raw_items):
        """Should calculate percentage of done items."""
        from src.processor import parse_items, calculate_metrics
        
        items = parse_items(sample_raw_items)
        metrics = calculate_metrics(items)
        
        assert metrics.completion_percentage == pytest.approx(33.3, rel=0.1)  # 1/3

    def test_should_calculate_planned_vs_unplanned(self, sample_raw_items):
        """Should count planned and unplanned items."""
        from src.processor import parse_items, calculate_metrics
        
        items = parse_items(sample_raw_items)
        metrics = calculate_metrics(items)
        
        assert metrics.planned_count == 2  # P1 items
        assert metrics.unplanned_count == 1  # P🔥 item
        assert metrics.unplanned_percentage == pytest.approx(33.3, rel=0.1)

    def test_should_count_high_priority_not_started(self):
        """Should count P🔥 and P0 items in Backlog or Todo."""
        from src.processor import parse_items, calculate_metrics
        
        raw_items = [
            {"id": "1", "title": "Fire Todo", "status": "Todo", "priority": "P🔥",
             "assignees": [], "estimate (Hrs)": None, "labels": [],
             "content": {"url": "https://github.com/test/repo/issues/1"}},
            {"id": "2", "title": "P0 Backlog", "status": "Backlog", "priority": "P0",
             "assignees": [], "estimate (Hrs)": None, "labels": [],
             "content": {"url": "https://github.com/test/repo/issues/2"}},
            {"id": "3", "title": "P0 In Progress", "status": "In Progress", "priority": "P0",
             "assignees": [], "estimate (Hrs)": None, "labels": [],
             "content": {"url": "https://github.com/test/repo/issues/3"}},
        ]
        
        items = parse_items(raw_items)
        metrics = calculate_metrics(items)
        
        assert metrics.high_priority_not_started == 2  # Fire Todo + P0 Backlog

    def test_should_handle_zero_items(self):
        """Should handle empty items list."""
        from src.processor import calculate_metrics
        
        metrics = calculate_metrics([])
        
        assert metrics.total_items == 0
        assert metrics.total_estimate_hours == 0.0
        assert metrics.completion_percentage == 0.0
        assert metrics.unplanned_percentage == 0.0

    def test_should_handle_items_without_estimates(self):
        """Should handle None estimate hours."""
        from src.processor import parse_items, calculate_metrics
        
        raw_items = [
            {"id": "1", "title": "No estimate", "status": "Todo", "priority": "P1",
             "assignees": [], "estimate (Hrs)": None, "labels": [],
             "content": {"url": "https://github.com/test/repo/issues/1"}},
        ]
        
        items = parse_items(raw_items)
        metrics = calculate_metrics(items)
        
        assert metrics.total_estimate_hours == 0.0



class TestDataGrouping:
    """Tests for data grouping functions."""

    def test_should_group_items_by_status(self, sample_raw_items):
        """Should group items by their status."""
        from src.processor import parse_items, group_by_status
        
        items = parse_items(sample_raw_items)
        grouped = group_by_status(items)
        
        assert "Todo" in grouped
        assert "In Progress" in grouped
        assert "Done" in grouped
        assert len(grouped["Todo"]) == 1
        assert len(grouped["In Progress"]) == 1
        assert len(grouped["Done"]) == 1

    def test_should_group_items_by_priority(self, sample_raw_items):
        """Should group items by their priority."""
        from src.processor import parse_items, group_by_priority
        
        items = parse_items(sample_raw_items)
        grouped = group_by_priority(items)
        
        assert "P🔥" in grouped
        assert "P1" in grouped
        assert len(grouped["P🔥"]) == 1
        assert len(grouped["P1"]) == 2

    def test_should_group_items_by_assignee(self, sample_raw_items):
        """Should group items by assignees."""
        from src.processor import parse_items, group_by_assignee
        
        items = parse_items(sample_raw_items)
        grouped = group_by_assignee(items)
        
        assert "user1" in grouped
        assert "user2" in grouped
        assert len(grouped["user1"]) == 2  # Items 1 and 3
        assert len(grouped["user2"]) == 1  # Item 2

    def test_should_handle_unassigned_items(self):
        """Should group unassigned items separately."""
        from src.processor import parse_items, group_by_assignee
        
        raw_items = [
            {"id": "1", "title": "Assigned", "status": "Todo", "priority": "P1",
             "assignees": ["user1"], "estimate (Hrs)": None, "labels": [],
             "content": {"url": "https://github.com/test/repo/issues/1"}},
            {"id": "2", "title": "Unassigned", "status": "Todo", "priority": "P1",
             "assignees": [], "estimate (Hrs)": None, "labels": [],
             "content": {"url": "https://github.com/test/repo/issues/2"}},
        ]
        
        items = parse_items(raw_items)
        grouped = group_by_assignee(items)
        
        assert "Unassigned" in grouped
        assert len(grouped["Unassigned"]) == 1

    def test_should_handle_items_with_multiple_assignees(self):
        """Should include item in each assignee's group."""
        from src.processor import parse_items, group_by_assignee
        
        raw_items = [
            {"id": "1", "title": "Multi", "status": "Todo", "priority": "P1",
             "assignees": ["user1", "user2"], "estimate (Hrs)": None, "labels": [],
             "content": {"url": "https://github.com/test/repo/issues/1"}},
        ]
        
        items = parse_items(raw_items)
        grouped = group_by_assignee(items)
        
        assert "user1" in grouped
        assert "user2" in grouped
        assert len(grouped["user1"]) == 1
        assert len(grouped["user2"]) == 1
        assert grouped["user1"][0].id == "1"
        assert grouped["user2"][0].id == "1"

    def test_should_return_empty_dict_for_empty_items(self):
        """Should return empty dict when no items."""
        from src.processor import group_by_status, group_by_priority, group_by_assignee
        
        assert group_by_status([]) == {}
        assert group_by_priority([]) == {}
        assert group_by_assignee([]) == {}



class TestColorCoding:
    """Tests for color coding logic."""

    def test_should_return_green_for_high_completion(self):
        """Should return green when completion > 70%."""
        from src.processor import get_completion_color
        
        assert get_completion_color(75.0) == "green"
        assert get_completion_color(100.0) == "green"
        assert get_completion_color(71.0) == "green"

    def test_should_return_red_for_low_completion(self):
        """Should return red when completion < 30%."""
        from src.processor import get_completion_color
        
        assert get_completion_color(25.0) == "red"
        assert get_completion_color(0.0) == "red"
        assert get_completion_color(29.0) == "red"

    def test_should_return_yellow_for_medium_completion(self):
        """Should return yellow when completion between 30-70%."""
        from src.processor import get_completion_color
        
        assert get_completion_color(50.0) == "yellow"
        assert get_completion_color(30.0) == "yellow"
        assert get_completion_color(70.0) == "yellow"

    def test_should_return_green_for_low_unplanned(self):
        """Should return green when unplanned < 10%."""
        from src.processor import get_unplanned_color
        
        assert get_unplanned_color(5.0) == "green"
        assert get_unplanned_color(0.0) == "green"
        assert get_unplanned_color(9.0) == "green"

    def test_should_return_red_for_high_unplanned(self):
        """Should return red when unplanned > 20%."""
        from src.processor import get_unplanned_color
        
        assert get_unplanned_color(25.0) == "red"
        assert get_unplanned_color(50.0) == "red"
        assert get_unplanned_color(21.0) == "red"

    def test_should_return_yellow_for_medium_unplanned(self):
        """Should return yellow when unplanned between 10-20%."""
        from src.processor import get_unplanned_color
        
        assert get_unplanned_color(15.0) == "yellow"
        assert get_unplanned_color(10.0) == "yellow"
        assert get_unplanned_color(20.0) == "yellow"

    def test_should_return_red_for_high_workload(self):
        """Should return red when workload > 10 items."""
        from src.processor import get_workload_color
        
        assert get_workload_color(11) == "red"
        assert get_workload_color(20) == "red"

    def test_should_return_yellow_for_medium_workload(self):
        """Should return yellow when workload 6-10 items."""
        from src.processor import get_workload_color
        
        assert get_workload_color(8) == "yellow"
        assert get_workload_color(6) == "yellow"
        assert get_workload_color(10) == "yellow"

    def test_should_return_green_for_low_workload(self):
        """Should return green when workload <= 5 items."""
        from src.processor import get_workload_color
        
        assert get_workload_color(5) == "green"
        assert get_workload_color(3) == "green"
        assert get_workload_color(0) == "green"

    def test_should_return_red_for_many_high_priority_not_started(self):
        """Should return red when high priority not started > 5."""
        from src.processor import get_high_priority_color
        
        assert get_high_priority_color(6) == "red"
        assert get_high_priority_color(10) == "red"

    def test_should_return_yellow_for_some_high_priority_not_started(self):
        """Should return yellow when high priority not started 1-5."""
        from src.processor import get_high_priority_color
        
        assert get_high_priority_color(3) == "yellow"
        assert get_high_priority_color(1) == "yellow"
        assert get_high_priority_color(5) == "yellow"

    def test_should_return_green_for_no_high_priority_not_started(self):
        """Should return green when high priority not started = 0."""
        from src.processor import get_high_priority_color
        
        assert get_high_priority_color(0) == "green"



class TestMetricsWithGrouping:
    """Tests for metrics calculation with grouped data."""

    def test_should_populate_items_by_status_in_metrics(self, sample_raw_items):
        """Metrics should include items grouped by status."""
        from src.processor import parse_items, calculate_metrics
        
        items = parse_items(sample_raw_items)
        metrics = calculate_metrics(items)
        
        assert "Todo" in metrics.items_by_status
        assert "In Progress" in metrics.items_by_status
        assert "Done" in metrics.items_by_status
        assert len(metrics.items_by_status["Todo"]) == 1
        assert len(metrics.items_by_status["In Progress"]) == 1
        assert len(metrics.items_by_status["Done"]) == 1

    def test_should_populate_items_by_priority_in_metrics(self, sample_raw_items):
        """Metrics should include items grouped by priority."""
        from src.processor import parse_items, calculate_metrics
        
        items = parse_items(sample_raw_items)
        metrics = calculate_metrics(items)
        
        assert "P🔥" in metrics.items_by_priority
        assert "P1" in metrics.items_by_priority
        assert len(metrics.items_by_priority["P🔥"]) == 1
        assert len(metrics.items_by_priority["P1"]) == 2

    def test_should_populate_items_by_assignee_in_metrics(self, sample_raw_items):
        """Metrics should include items grouped by assignee."""
        from src.processor import parse_items, calculate_metrics
        
        items = parse_items(sample_raw_items)
        metrics = calculate_metrics(items)
        
        assert "user1" in metrics.items_by_assignee
        assert "user2" in metrics.items_by_assignee
        assert len(metrics.items_by_assignee["user1"]) == 2
        assert len(metrics.items_by_assignee["user2"]) == 1

    def test_should_handle_empty_items_list_with_grouping(self):
        """Metrics should handle empty items list gracefully."""
        from src.processor import calculate_metrics
        
        metrics = calculate_metrics([])
        
        assert metrics.items_by_status == {}
        assert metrics.items_by_priority == {}
        assert metrics.items_by_assignee == {}



class TestInvalidDataHandling:
    """Tests for handling invalid or malformed data."""

    def test_should_handle_invalid_priority_value(self):
        """Should default to P2 for truly invalid priority values."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "Todo",
            "priority": "InvalidPriority",  # Doesn't start with P
            "assignees": [],
            "estimate (Hrs)": None,
            "labels": [],
            "content": {"url": ""}
        }
        
        item = parse_item(raw_item)
        
        assert item.priority.value == "P2"

    def test_should_handle_invalid_status_value(self):
        """Should default to Backlog for invalid status values."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "InvalidStatus",
            "priority": "P1",
            "assignees": [],
            "estimate (Hrs)": None,
            "labels": [],
            "content": {"url": ""}
        }
        
        item = parse_item(raw_item)
        
        assert item.status.value == "Backlog"

    def test_should_handle_corrupted_fire_emoji(self):
        """Should recognize corrupted P🔥 emoji as FIRE priority."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "Todo",
            "priority": "P≡ا¤ح",  # Corrupted P🔥 from real data
            "assignees": [],
            "estimate (Hrs)": None,
            "labels": [],
            "content": {"url": ""}
        }
        
        item = parse_item(raw_item)
        
        assert item.priority.value == "P🔥"
    
    def test_should_handle_various_corrupted_fire_formats(self):
        """Should handle various corrupted fire emoji formats."""
        from src.processor import parse_item
        from src.models import Priority
        
        corrupted_values = ["Pًں\"¥", "P≡ا¤ح", "P🔥corrupted", "P█î"]
        
        for corrupted in corrupted_values:
            raw_item = {
                "id": "1",
                "title": "Test",
                "status": "Todo",
                "priority": corrupted,
                "assignees": [],
                "estimate (Hrs)": None,
                "labels": [],
                "content": {"url": ""}
            }
            
            item = parse_item(raw_item)
            
            # All corrupted P-something should be treated as FIRE
            assert item.priority == Priority.FIRE, f"Failed for: {corrupted}"

    def test_should_handle_empty_priority(self):
        """Should handle empty priority value."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "Todo",
            "priority": "",
            "assignees": [],
            "estimate (Hrs)": None,
            "labels": [],
            "content": {"url": ""}
        }
        
        item = parse_item(raw_item)
        
        assert item.priority.value == "P2"

    def test_should_handle_none_priority(self):
        """Should handle None priority value."""
        from src.processor import parse_item
        
        raw_item = {
            "id": "1",
            "title": "Test",
            "status": "Todo",
            "priority": None,
            "assignees": [],
            "estimate (Hrs)": None,
            "labels": [],
            "content": {"url": ""}
        }
        
        item = parse_item(raw_item)
        
        assert item.priority.value == "P2"


# Tests for enhanced metrics (Task 1.4)

def test_calculate_todo_count():
    """Test todo count calculation."""
    from src.processor import calculate_todo_count
    
    items = [
        ProjectItem(
            id="1", title="Task 1", status=Status.TODO, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="2", title="Task 2", status=Status.TODO, priority=Priority.P2,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="3", title="Task 3", status=Status.IN_PROGRESS, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="4", title="Task 4", status=Status.DONE, priority=Priority.P2,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
    ]
    
    result = calculate_todo_count(items)
    assert result == 2, f"Expected 2 todo items, got {result}"


def test_calculate_done_active_count():
    """Test done active count excludes backlog."""
    from src.processor import calculate_done_active_count
    
    items = [
        ProjectItem(
            id="1", title="Task 1", status=Status.DONE, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="2", title="Task 2", status=Status.DONE, priority=Priority.P2,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="3", title="Task 3", status=Status.TODO, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
    ]
    
    result = calculate_done_active_count(items)
    assert result == 2, f"Expected 2 done items, got {result}"


def test_calculate_unplanned_done_percentage():
    """Test unplanned done percentage with various ratios."""
    from src.processor import calculate_unplanned_done_stats
    
    # Test with 50% unplanned done
    items = [
        ProjectItem(
            id="1", title="Task 1", status=Status.DONE, priority=Priority.FIRE,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="2", title="Task 2", status=Status.DONE, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="3", title="Task 3", status=Status.TODO, priority=Priority.FIRE,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
    ]
    
    percentage, count = calculate_unplanned_done_stats(items)
    assert percentage == 50.0, f"Expected 50.0%, got {percentage}%"
    assert count == 1, f"Expected 1 unplanned done, got {count}"


def test_calculate_unplanned_done_percentage_zero_done():
    """Test unplanned done percentage when no done items exist."""
    from src.processor import calculate_unplanned_done_stats
    
    items = [
        ProjectItem(
            id="1", title="Task 1", status=Status.TODO, priority=Priority.FIRE,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="2", title="Task 2", status=Status.IN_PROGRESS, priority=Priority.P1,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
    ]
    
    percentage, count = calculate_unplanned_done_stats(items)
    assert percentage == 0.0, f"Expected 0.0%, got {percentage}%"
    assert count == 0, f"Expected 0 unplanned done, got {count}"


def test_calculate_unplanned_done_percentage_all_unplanned():
    """Test unplanned done percentage when all done items are unplanned."""
    from src.processor import calculate_unplanned_done_stats
    
    items = [
        ProjectItem(
            id="1", title="Task 1", status=Status.DONE, priority=Priority.FIRE,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="2", title="Task 2", status=Status.DONE, priority=Priority.FIRE,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="3", title="Task 3", status=Status.DONE, priority=Priority.FIRE,
            assignees=[], estimate_hours=None, labels=[], url="", repository="", issue_number=None
        ),
    ]
    
    percentage, count = calculate_unplanned_done_stats(items)
    assert percentage == 100.0, f"Expected 100.0%, got {percentage}%"
    assert count == 3, f"Expected 3 unplanned done, got {count}"


def test_enhanced_metrics_in_calculate_metrics():
    """Test that enhanced metrics are included in calculate_metrics output."""
    from src.processor import calculate_metrics
    
    items = [
        ProjectItem(
            id="1", title="Task 1", status=Status.TODO, priority=Priority.P1,
            assignees=["Alice"], estimate_hours=5.0, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="2", title="Task 2", status=Status.DONE, priority=Priority.FIRE,
            assignees=["Bob"], estimate_hours=3.0, labels=[], url="", repository="", issue_number=None
        ),
        ProjectItem(
            id="3", title="Task 3", status=Status.DONE, priority=Priority.P2,
            assignees=["Alice"], estimate_hours=2.0, labels=[], url="", repository="", issue_number=None
        ),
    ]
    
    metrics = calculate_metrics(items)
    
    # Verify new fields exist and have correct values
    assert hasattr(metrics, 'todo_items'), "Missing todo_items field"
    assert hasattr(metrics, 'done_active_items'), "Missing done_active_items field"
    assert hasattr(metrics, 'unplanned_done_percentage'), "Missing unplanned_done_percentage field"
    assert hasattr(metrics, 'unplanned_done_count'), "Missing unplanned_done_count field"
    
    assert metrics.todo_items == 1, f"Expected 1 todo item, got {metrics.todo_items}"
    assert metrics.done_active_items == 2, f"Expected 2 done items, got {metrics.done_active_items}"
    assert metrics.unplanned_done_percentage == 50.0, f"Expected 50.0%, got {metrics.unplanned_done_percentage}%"
    assert metrics.unplanned_done_count == 1, f"Expected 1 unplanned done, got {metrics.unplanned_done_count}"
