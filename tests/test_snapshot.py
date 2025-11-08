"""Tests for snapshot management."""

import pytest
import json
from pathlib import Path
from datetime import datetime


class TestSnapshotSave:
    """Tests for snapshot save functionality."""

    def test_should_create_snapshots_directory_if_not_exists(self, tmp_path):
        """Should create snapshots directory when saving."""
        from src.snapshot import save_snapshot
        from src.models import ProjectItem, Priority, Status
        
        items = [
            ProjectItem(
                id="1", title="Test", status=Status.TODO, priority=Priority.P1,
                assignees=["user1"], estimate_hours=5.0, labels=["bug"],
                url="https://github.com/test/repo/issues/1",
                repository="test/repo", issue_number=1
            )
        ]
        
        snapshot_dir = tmp_path / "snapshots"
        save_snapshot(items, snapshot_dir=str(snapshot_dir))
        
        assert snapshot_dir.exists()
        assert snapshot_dir.is_dir()

    def test_should_save_snapshot_with_timestamp_filename(self, tmp_path):
        """Should save snapshot with format snapshot-YYYYMMDD-HHMMSS.json."""
        from src.snapshot import save_snapshot
        from src.models import ProjectItem, Priority, Status
        
        items = [
            ProjectItem(
                id="1", title="Test", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        snapshot_dir = tmp_path / "snapshots"
        filepath = save_snapshot(items, snapshot_dir=str(snapshot_dir))
        
        # Check filename format
        filename = Path(filepath).name
        assert filename.startswith("snapshot-")
        assert filename.endswith(".json")
        assert len(filename) == len("snapshot-YYYYMMDD-HHMMSS.json")

    def test_should_save_items_as_json(self, tmp_path):
        """Should save items data in JSON format."""
        from src.snapshot import save_snapshot
        from src.models import ProjectItem, Priority, Status
        
        items = [
            ProjectItem(
                id="1", title="Test Item", status=Status.TODO, priority=Priority.P1,
                assignees=["user1"], estimate_hours=5.0, labels=["bug"],
                url="https://github.com/test/repo/issues/1",
                repository="test/repo", issue_number=1
            )
        ]
        
        snapshot_dir = tmp_path / "snapshots"
        filepath = save_snapshot(items, snapshot_dir=str(snapshot_dir))
        
        # Read and verify JSON
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "timestamp" in data
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["id"] == "1"
        assert data["items"][0]["title"] == "Test Item"

    def test_should_include_timestamp_in_snapshot(self, tmp_path):
        """Should include ISO format timestamp in snapshot data."""
        from src.snapshot import save_snapshot
        from src.models import ProjectItem, Priority, Status
        
        items = [
            ProjectItem(
                id="1", title="Test", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        snapshot_dir = tmp_path / "snapshots"
        filepath = save_snapshot(items, snapshot_dir=str(snapshot_dir))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "timestamp" in data
        # Verify it's a valid ISO format timestamp
        datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))

    def test_should_serialize_all_item_fields(self, tmp_path):
        """Should serialize all ProjectItem fields correctly."""
        from src.snapshot import save_snapshot
        from src.models import ProjectItem, Priority, Status
        
        items = [
            ProjectItem(
                id="PVTI_123",
                title="Test Task",
                status=Status.IN_PROGRESS,
                priority=Priority.FIRE,
                assignees=["user1", "user2"],
                estimate_hours=8.5,
                labels=["urgent", "bug"],
                url="https://github.com/test/repo/issues/42",
                repository="test/repo",
                issue_number=42
            )
        ]
        
        snapshot_dir = tmp_path / "snapshots"
        filepath = save_snapshot(items, snapshot_dir=str(snapshot_dir))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        item = data["items"][0]
        assert item["id"] == "PVTI_123"
        assert item["title"] == "Test Task"
        assert item["status"] == "In Progress"
        assert item["priority"] == "P🔥"
        assert item["assignees"] == ["user1", "user2"]
        assert item["estimate_hours"] == 8.5
        assert item["labels"] == ["urgent", "bug"]
        assert item["url"] == "https://github.com/test/repo/issues/42"
        assert item["repository"] == "test/repo"
        assert item["issue_number"] == 42

    def test_should_handle_empty_items_list(self, tmp_path):
        """Should handle saving empty items list."""
        from src.snapshot import save_snapshot
        
        snapshot_dir = tmp_path / "snapshots"
        filepath = save_snapshot([], snapshot_dir=str(snapshot_dir))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data["items"] == []
        assert "timestamp" in data

    def test_should_return_filepath(self, tmp_path):
        """Should return the path to saved snapshot file."""
        from src.snapshot import save_snapshot
        from src.models import ProjectItem, Priority, Status
        
        items = [
            ProjectItem(
                id="1", title="Test", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        snapshot_dir = tmp_path / "snapshots"
        filepath = save_snapshot(items, snapshot_dir=str(snapshot_dir))
        
        assert Path(filepath).exists()
        assert Path(filepath).is_file()



class TestSnapshotComparison:
    """Tests for snapshot comparison logic."""

    def test_should_load_previous_snapshot(self, tmp_path):
        """Should load the most recent snapshot from directory."""
        from src.snapshot import save_snapshot, load_latest_snapshot
        from src.models import ProjectItem, Priority, Status
        
        items = [
            ProjectItem(
                id="1", title="Test", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        snapshot_dir = tmp_path / "snapshots"
        save_snapshot(items, snapshot_dir=str(snapshot_dir))
        
        loaded_items = load_latest_snapshot(snapshot_dir=str(snapshot_dir))
        
        assert loaded_items is not None
        assert len(loaded_items) == 1
        assert loaded_items[0].id == "1"

    def test_should_return_none_when_no_snapshots_exist(self, tmp_path):
        """Should return None when no previous snapshots exist."""
        from src.snapshot import load_latest_snapshot
        
        snapshot_dir = tmp_path / "snapshots"
        snapshot_dir.mkdir()
        
        loaded_items = load_latest_snapshot(snapshot_dir=str(snapshot_dir))
        
        assert loaded_items is None

    def test_should_load_most_recent_snapshot(self, tmp_path):
        """Should load the most recent snapshot when multiple exist."""
        from src.snapshot import save_snapshot, load_latest_snapshot
        from src.models import ProjectItem, Priority, Status
        import time
        
        snapshot_dir = tmp_path / "snapshots"
        
        # Save first snapshot
        items1 = [
            ProjectItem(
                id="1", title="Old", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        save_snapshot(items1, snapshot_dir=str(snapshot_dir))
        
        time.sleep(0.1)  # Ensure different timestamp
        
        # Save second snapshot
        items2 = [
            ProjectItem(
                id="2", title="New", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        save_snapshot(items2, snapshot_dir=str(snapshot_dir))
        
        loaded_items = load_latest_snapshot(snapshot_dir=str(snapshot_dir))
        
        assert loaded_items[0].id == "2"
        assert loaded_items[0].title == "New"

    def test_should_calculate_items_completed_since_last_snapshot(self):
        """Should count items that moved to Done status."""
        from src.snapshot import compare_snapshots
        from src.models import ProjectItem, Priority, Status
        
        previous = [
            ProjectItem(
                id="1", title="Item 1", status=Status.IN_PROGRESS, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            ),
            ProjectItem(
                id="2", title="Item 2", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        current = [
            ProjectItem(
                id="1", title="Item 1", status=Status.DONE, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            ),
            ProjectItem(
                id="2", title="Item 2", status=Status.DONE, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        comparison = compare_snapshots(current, previous)
        
        assert comparison["items_completed"] == 2

    def test_should_calculate_new_items_added(self):
        """Should count items that didn't exist in previous snapshot."""
        from src.snapshot import compare_snapshots
        from src.models import ProjectItem, Priority, Status
        
        previous = [
            ProjectItem(
                id="1", title="Item 1", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        current = [
            ProjectItem(
                id="1", title="Item 1", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            ),
            ProjectItem(
                id="2", title="Item 2", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            ),
            ProjectItem(
                id="3", title="Item 3", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        comparison = compare_snapshots(current, previous)
        
        assert comparison["items_added"] == 2

    def test_should_track_status_changes(self):
        """Should track items that changed status."""
        from src.snapshot import compare_snapshots
        from src.models import ProjectItem, Priority, Status
        
        previous = [
            ProjectItem(
                id="1", title="Item 1", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            ),
            ProjectItem(
                id="2", title="Item 2", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        current = [
            ProjectItem(
                id="1", title="Item 1", status=Status.IN_PROGRESS, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            ),
            ProjectItem(
                id="2", title="Item 2", status=Status.DONE, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        comparison = compare_snapshots(current, previous)
        
        assert "status_changes" in comparison
        assert len(comparison["status_changes"]) == 2

    def test_should_handle_comparison_with_no_previous_snapshot(self):
        """Should handle comparison when previous is None."""
        from src.snapshot import compare_snapshots
        from src.models import ProjectItem, Priority, Status
        
        current = [
            ProjectItem(
                id="1", title="Item 1", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        comparison = compare_snapshots(current, None)
        
        assert comparison["items_completed"] == 0
        assert comparison["items_added"] == 0
        assert comparison["status_changes"] == []

    def test_should_handle_empty_current_snapshot(self):
        """Should handle comparison with empty current items."""
        from src.snapshot import compare_snapshots
        from src.models import ProjectItem, Priority, Status
        
        previous = [
            ProjectItem(
                id="1", title="Item 1", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        comparison = compare_snapshots([], previous)
        
        assert comparison["items_completed"] == 0
        assert comparison["items_added"] == 0
