"""Integration tests for end-to-end workflows."""

import pytest
from pathlib import Path
import json

from src.models import ProjectItem, Priority, Status
from src.processor import parse_items, calculate_metrics
from src.snapshot import save_snapshot, load_latest_snapshot, compare_snapshots
from src.renderers.html_renderer import HTMLRenderer
from src.renderers.md_renderer import MarkdownRenderer
from src.renderers.csv_renderer import CSVRenderer
from src.renderers.json_renderer import JSONRenderer


@pytest.fixture
def sample_project_data():
    """Provide sample project data for integration tests."""
    return [
        {
            "id": "1",
            "title": "Implement user authentication",
            "status": "In Progress",
            "priority": "P0",
            "assignees": ["user1"],
            "estimate (Hrs)": 8.0,
            "labels": ["feature", "security"],
            "content": {
                "url": "https://github.com/test/repo/issues/1",
                "repository": "test/repo",
                "number": 1
            }
        },
        {
            "id": "2",
            "title": "Fix critical bug",
            "status": "Todo",
            "priority": "P🔥",
            "assignees": ["user2"],
            "estimate (Hrs)": 3.0,
            "labels": ["bug", "urgent"],
            "content": {
                "url": "https://github.com/test/repo/issues/2",
                "repository": "test/repo",
                "number": 2
            }
        },
        {
            "id": "3",
            "title": "Update documentation",
            "status": "Done",
            "priority": "P2",
            "assignees": ["user1", "user3"],
            "estimate (Hrs)": 2.0,
            "labels": ["docs"],
            "content": {
                "url": "https://github.com/test/repo/issues/3",
                "repository": "test/repo",
                "number": 3
            }
        }
    ]


class TestEndToEndWorkflow:
    """Test complete end-to-end workflow."""

    def test_should_process_and_generate_all_formats(self, tmp_path, sample_project_data):
        """Should process data and generate reports in all formats."""
        # Parse items
        items = parse_items(sample_project_data)
        assert len(items) == 3
        
        # Calculate metrics
        metrics = calculate_metrics(items)
        assert metrics.total_items == 3
        assert metrics.completion_percentage == pytest.approx(33.33, rel=0.1)
        assert metrics.unplanned_count == 1
        
        # Generate HTML report
        html_path = tmp_path / "report.html"
        html_renderer = HTMLRenderer()
        html_renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(html_path),
            project_name="Test Project",
            owner="TestOrg",
            project_number=1
        )
        assert html_path.exists()
        html_content = html_path.read_text(encoding='utf-8')
        assert 'Test Project' in html_content
        assert 'dir="rtl"' in html_content
        
        # Generate Markdown report
        md_path = tmp_path / "report.md"
        md_renderer = MarkdownRenderer()
        md_renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(md_path),
            project_name="Test Project",
            owner="TestOrg",
            project_number=1
        )
        assert md_path.exists()
        md_content = md_path.read_text(encoding='utf-8')
        assert '# گزارش پروژه' in md_content
        
        # Generate CSV report
        csv_path = tmp_path / "report.csv"
        csv_renderer = CSVRenderer()
        csv_renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(csv_path),
            project_name="Test Project",
            owner="TestOrg",
            project_number=1
        )
        assert csv_path.exists()
        
        # Generate JSON report
        json_path = tmp_path / "report.json"
        json_renderer = JSONRenderer()
        json_renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(json_path),
            project_name="Test Project",
            owner="TestOrg",
            project_number=1
        )
        assert json_path.exists()
        json_data = json.loads(json_path.read_text(encoding='utf-8'))
        assert json_data['metadata']['project_name'] == 'Test Project'
        assert json_data['metrics']['total_items'] == 3

    def test_should_handle_snapshot_workflow(self, tmp_path, sample_project_data):
        """Should save and compare snapshots."""
        # Parse items
        items = parse_items(sample_project_data)
        
        # Save first snapshot
        snapshot_dir = tmp_path / "snapshots"
        snapshot_path1 = save_snapshot(items, snapshot_dir=str(snapshot_dir))
        assert Path(snapshot_path1).exists()
        
        # Load snapshot
        loaded_items = load_latest_snapshot(snapshot_dir=str(snapshot_dir))
        assert loaded_items is not None
        assert len(loaded_items) == 3
        
        # Modify data (complete an item)
        sample_project_data[0]['status'] = 'Done'
        items_updated = parse_items(sample_project_data)
        
        # Compare snapshots
        comparison = compare_snapshots(items_updated, items)
        assert comparison['items_completed'] == 1
        assert comparison['items_added'] == 0

    def test_should_handle_persian_text_throughout(self, tmp_path):
        """Should handle Persian text in all components."""
        # Create items with Persian text
        persian_data = [
            {
                "id": "1",
                "title": "پیاده‌سازی احراز هویت کاربر",
                "status": "In Progress",
                "priority": "P1",
                "assignees": ["کاربر۱"],
                "estimate (Hrs)": 5.0,
                "labels": ["ویژگی"],
                "content": {
                    "url": "https://github.com/test/repo/issues/1",
                    "repository": "test/repo",
                    "number": 1
                }
            }
        ]
        
        items = parse_items(persian_data)
        metrics = calculate_metrics(items)
        
        # Test HTML rendering with Persian
        html_path = tmp_path / "persian_report.html"
        html_renderer = HTMLRenderer()
        html_renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(html_path),
            project_name="پروژه تست",
            owner="سازمان",
            project_number=1
        )
        
        html_content = html_path.read_text(encoding='utf-8')
        assert 'پیاده‌سازی احراز هویت کاربر' in html_content
        assert 'پروژه تست' in html_content
        assert 'کاربر۱' in html_content

    def test_should_handle_empty_project(self, tmp_path):
        """Should handle project with no items."""
        items = []
        metrics = calculate_metrics(items)
        
        assert metrics.total_items == 0
        assert metrics.completion_percentage == 0.0
        
        # Should still generate reports
        html_path = tmp_path / "empty_report.html"
        html_renderer = HTMLRenderer()
        html_renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(html_path),
            project_name="Empty Project",
            owner="TestOrg",
            project_number=1
        )
        
        assert html_path.exists()

    def test_should_handle_large_dataset(self, tmp_path):
        """Should handle projects with many items."""
        # Create 100 items
        large_dataset = []
        for i in range(100):
            large_dataset.append({
                "id": str(i),
                "title": f"Task {i}",
                "status": "Todo" if i % 3 == 0 else "In Progress" if i % 3 == 1 else "Done",
                "priority": "P1",
                "assignees": [f"user{i % 5}"],
                "estimate (Hrs)": float(i % 10 + 1),
                "labels": ["test"],
                "content": {
                    "url": f"https://github.com/test/repo/issues/{i}",
                    "repository": "test/repo",
                    "number": i
                }
            })
        
        items = parse_items(large_dataset)
        metrics = calculate_metrics(items)
        
        assert metrics.total_items == 100
        
        # Generate report
        html_path = tmp_path / "large_report.html"
        html_renderer = HTMLRenderer()
        html_renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(html_path),
            project_name="Large Project",
            owner="TestOrg",
            project_number=1
        )
        
        assert html_path.exists()
        # File should be reasonably sized
        assert html_path.stat().st_size > 0
