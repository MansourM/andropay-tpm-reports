"""HTML report renderer using Jinja2."""

from pathlib import Path
from typing import List
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from src.models import ProjectItem, ProjectMetrics, Priority
from src.charts.chart_builder import ChartBuilder
from src.processor import (
    get_completion_color,
    get_unplanned_color,
    get_high_priority_color
)


def get_unplanned_done_color(percentage: float) -> str:
    """
    Get color for unplanned done percentage.
    
    Lower is better - indicates better planning accuracy.
    
    Args:
        percentage: Unplanned done percentage (0-100)
        
    Returns:
        Color name: 'green', 'yellow', or 'red'
    """
    if percentage < 20:
        return "green"
    elif percentage > 40:
        return "red"
    else:
        return "yellow"


class HTMLRenderer:
    """Renderer for generating HTML reports."""
    
    def __init__(self):
        """Initialize HTMLRenderer with Jinja2 environment."""
        # Set up Jinja2 environment
        template_dir = Path(__file__).parent.parent / 'templates'
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=True
        )
        self.template = self.env.get_template('report.html')
        self.chart_builder = ChartBuilder()
    
    def render(
        self,
        items: List[ProjectItem],
        metrics: ProjectMetrics,
        output_path: str,
        project_name: str = "GitHub Project",
        owner: str = "",
        project_number: int = 0
    ) -> None:
        """
        Render HTML report and save to file.
        
        Args:
            items: List of all project items
            metrics: Calculated project metrics
            output_path: Path to save the HTML file
            project_name: Name of the project
            owner: GitHub organization/user
            project_number: Project number
        """
        # Filter high priority items (P🔥 and P0)
        high_priority_items = [
            item for item in items
            if item.priority in [Priority.FIRE, Priority.P0]
        ]
        
        # Sort high priority items by priority (FIRE first, then P0)
        high_priority_items.sort(
            key=lambda x: (0 if x.priority == Priority.FIRE else 1, x.title)
        )
        
        # Generate charts
        status_counts = {
            status: len(items_list)
            for status, items_list in metrics.items_by_status.items()
        }
        
        priority_counts = {
            priority: len(items_list)
            for priority, items_list in metrics.items_by_priority.items()
        }
        
        # Count active items per assignee for workload (exclude MansourM - TPM)
        assignee_workload = {}
        for assignee, assignee_items in metrics.items_by_assignee.items():
            # Skip MansourM (TPM - not a developer)
            if assignee == "MansourM":
                continue
            active_count = sum(1 for item in assignee_items if item.is_active)
            if active_count > 0:  # Only include assignees with active items
                assignee_workload[assignee] = active_count
        
        # Generate chart JSON
        status_pie_chart = self.chart_builder.create_status_pie_chart(status_counts)
        priority_chart = self.chart_builder.create_priority_chart(priority_counts)
        planned_unplanned_chart = self.chart_builder.create_planned_vs_unplanned_chart(
            metrics.planned_count,
            metrics.unplanned_count
        )
        team_workload_chart = self.chart_builder.create_team_workload_chart(assignee_workload)
        
        # Determine colors for metrics
        completion_color = get_completion_color(metrics.active_completion_percentage)
        unplanned_color = get_unplanned_color(metrics.unplanned_percentage)
        active_unplanned_color = get_unplanned_color(metrics.active_unplanned_percentage)
        high_priority_color = get_high_priority_color(metrics.high_priority_not_started)
        unplanned_done_color = get_unplanned_done_color(metrics.unplanned_done_percentage)
        
        # Prepare template context
        context = {
            'project_name': project_name,
            'owner': owner,
            'project_number': project_number,
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'metrics': metrics,
            'completion_color': completion_color,
            'unplanned_color': unplanned_color,
            'active_unplanned_color': active_unplanned_color,
            'high_priority_color': high_priority_color,
            'unplanned_done_color': unplanned_done_color,
            'high_priority_items': high_priority_items,
            'items_by_status': metrics.items_by_status,
            'all_items': items,
            'status_pie_chart': status_pie_chart,
            'priority_chart': priority_chart,
            'planned_unplanned_chart': planned_unplanned_chart,
            'team_workload_chart': team_workload_chart
        }
        
        # Render template
        html_content = self.template.render(**context)
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding='utf-8')
