"""Tests for HTML renderer."""

import pytest
from pathlib import Path


class TestHTMLRenderer:
    """Tests for HTMLRenderer class."""

    def test_should_create_html_renderer(self):
        """Should create HTMLRenderer instance."""
        from src.renderers.html_renderer import HTMLRenderer
        
        renderer = HTMLRenderer()
        
        assert renderer is not None

    def test_should_load_template(self):
        """Should load Jinja2 template."""
        from src.renderers.html_renderer import HTMLRenderer
        
        renderer = HTMLRenderer()
        
        assert renderer.template is not None

    def test_should_render_html_with_basic_data(self, tmp_path):
        """Should render HTML with project data."""
        from src.renderers.html_renderer import HTMLRenderer
        from src.models import ProjectItem, ProjectMetrics, Priority, Status
        
        renderer = HTMLRenderer()
        
        items = [
            ProjectItem(
                id="1", title="Test Item", status=Status.TODO, priority=Priority.P1,
                assignees=["user1"], estimate_hours=5.0, labels=["bug"],
                url="https://github.com/test/repo/issues/1",
                repository="test/repo", issue_number=1
            )
        ]
        
        metrics = ProjectMetrics(
            total_items=1,
            total_estimate_hours=5.0,
            completion_percentage=0.0,
            planned_count=1,
            unplanned_count=0,
            unplanned_percentage=0.0,
            high_priority_not_started=1,
            items_by_status={"Todo": items},
            items_by_priority={"P1": items},
            items_by_assignee={"user1": items}
        )
        
        output_file = tmp_path / "test_report.html"
        renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(output_file),
            project_name="Test Project",
            owner="TestOrg",
            project_number=1
        )
        
        assert output_file.exists()
        content = output_file.read_text(encoding='utf-8')
        assert 'Test Project' in content
        assert 'Test Item' in content

    def test_should_include_rtl_direction(self, tmp_path):
        """Should include RTL direction in HTML."""
        from src.renderers.html_renderer import HTMLRenderer
        from src.models import ProjectMetrics
        
        renderer = HTMLRenderer()
        
        metrics = ProjectMetrics(
            total_items=0, total_estimate_hours=0.0, completion_percentage=0.0,
            planned_count=0, unplanned_count=0, unplanned_percentage=0.0,
            high_priority_not_started=0, items_by_status={},
            items_by_priority={}, items_by_assignee={}
        )
        
        output_file = tmp_path / "test_report.html"
        renderer.render(
            items=[],
            metrics=metrics,
            output_path=str(output_file),
            project_name="Test",
            owner="Test",
            project_number=1
        )
        
        content = output_file.read_text(encoding='utf-8')
        assert 'dir="rtl"' in content
        assert 'lang="fa"' in content

    def test_should_include_charts_data(self, tmp_path):
        """Should include chart data in rendered HTML."""
        from src.renderers.html_renderer import HTMLRenderer
        from src.models import ProjectItem, ProjectMetrics, Priority, Status
        
        renderer = HTMLRenderer()
        
        items = [
            ProjectItem(
                id="1", title="Test", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        metrics = ProjectMetrics(
            total_items=1, total_estimate_hours=0.0, completion_percentage=0.0,
            planned_count=1, unplanned_count=0, unplanned_percentage=0.0,
            high_priority_not_started=1,
            items_by_status={"Todo": items},
            items_by_priority={"P1": items},
            items_by_assignee={}
        )
        
        output_file = tmp_path / "test_report.html"
        renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(output_file),
            project_name="Test",
            owner="Test",
            project_number=1
        )
        
        content = output_file.read_text(encoding='utf-8')
        assert 'chartData' in content
        assert 'Plotly' in content

    def test_should_apply_color_coding_to_metrics(self, tmp_path):
        """Should apply color coding based on metric values."""
        from src.renderers.html_renderer import HTMLRenderer
        from src.models import ProjectMetrics
        
        renderer = HTMLRenderer()
        
        metrics = ProjectMetrics(
            total_items=10, total_estimate_hours=50.0,
            completion_percentage=80.0,  # Should be green
            planned_count=9, unplanned_count=1,
            unplanned_percentage=10.0,  # Should be yellow
            high_priority_not_started=0,  # Should be green
            items_by_status={}, items_by_priority={}, items_by_assignee={}
        )
        
        output_file = tmp_path / "test_report.html"
        renderer.render(
            items=[],
            metrics=metrics,
            output_path=str(output_file),
            project_name="Test",
            owner="Test",
            project_number=1
        )
        
        content = output_file.read_text(encoding='utf-8')
        assert 'metric-green' in content or 'green' in content

    def test_should_filter_high_priority_items(self, tmp_path):
        """Should filter and display only P🔥 and P0 items."""
        from src.renderers.html_renderer import HTMLRenderer
        from src.models import ProjectItem, ProjectMetrics, Priority, Status
        
        renderer = HTMLRenderer()
        
        items = [
            ProjectItem(
                id="1", title="Fire Item", status=Status.TODO, priority=Priority.FIRE,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            ),
            ProjectItem(
                id="2", title="P0 Item", status=Status.TODO, priority=Priority.P0,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            ),
            ProjectItem(
                id="3", title="P1 Item", status=Status.TODO, priority=Priority.P1,
                assignees=[], estimate_hours=None, labels=[],
                url="", repository="", issue_number=None
            )
        ]
        
        metrics = ProjectMetrics(
            total_items=3, total_estimate_hours=0.0, completion_percentage=0.0,
            planned_count=2, unplanned_count=1, unplanned_percentage=33.3,
            high_priority_not_started=2,
            items_by_status={}, items_by_priority={}, items_by_assignee={}
        )
        
        output_file = tmp_path / "test_report.html"
        renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(output_file),
            project_name="Test",
            owner="Test",
            project_number=1
        )
        
        content = output_file.read_text(encoding='utf-8')
        assert 'Fire Item' in content
        assert 'P0 Item' in content

    def test_should_use_utf8_encoding(self, tmp_path):
        """Should use UTF-8 encoding for Persian text."""
        from src.renderers.html_renderer import HTMLRenderer
        from src.models import ProjectItem, ProjectMetrics, Priority, Status
        
        renderer = HTMLRenderer()
        
        items = [
            ProjectItem(
                id="1", title="تسک تست", status=Status.TODO, priority=Priority.P1,
                assignees=["کاربر"], estimate_hours=5.0, labels=["باگ"],
                url="", repository="", issue_number=None
            )
        ]
        
        metrics = ProjectMetrics(
            total_items=1, total_estimate_hours=5.0, completion_percentage=0.0,
            planned_count=1, unplanned_count=0, unplanned_percentage=0.0,
            high_priority_not_started=1,
            items_by_status={}, items_by_priority={}, items_by_assignee={}
        )
        
        output_file = tmp_path / "test_report.html"
        renderer.render(
            items=items,
            metrics=metrics,
            output_path=str(output_file),
            project_name="پروژه تست",
            owner="سازمان",
            project_number=1
        )
        
        content = output_file.read_text(encoding='utf-8')
        assert 'تسک تست' in content
        assert 'پروژه تست' in content
        assert 'charset="UTF-8"' in content
