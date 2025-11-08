"""JSON report renderer."""

import json
from pathlib import Path
from typing import List
from datetime import datetime

from src.renderers.base import Renderer
from src.models import ProjectItem, ProjectMetrics


class JSONRenderer(Renderer):
    """Renderer for generating JSON reports."""
    
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
        Render JSON report and save to file.
        
        Args:
            items: List of all project items
            metrics: Calculated project metrics
            output_path: Path to save the JSON file
            project_name: Name of the project
            owner: GitHub organization/user
            project_number: Project number
        """
        # Prepare data structure
        data = {
            'metadata': {
                'project_name': project_name,
                'owner': owner,
                'project_number': project_number,
                'generation_timestamp': datetime.now().isoformat() + 'Z',
                'total_items': metrics.total_items
            },
            'metrics': {
                'total_items': metrics.total_items,
                'total_estimate_hours': metrics.total_estimate_hours,
                'completion_percentage': metrics.completion_percentage,
                'planned_count': metrics.planned_count,
                'unplanned_count': metrics.unplanned_count,
                'unplanned_percentage': metrics.unplanned_percentage,
                'high_priority_not_started': metrics.high_priority_not_started
            },
            'items': [
                {
                    'id': item.id,
                    'title': item.title,
                    'status': item.status.value,
                    'priority': item.priority.value,
                    'assignees': item.assignees,
                    'estimate_hours': item.estimate_hours,
                    'labels': item.labels,
                    'url': item.url,
                    'repository': item.repository,
                    'issue_number': item.issue_number,
                    'is_planned': item.is_planned,
                    'is_active': item.is_active
                }
                for item in items
            ],
            'grouped_data': {
                'by_status': {
                    status: len(items_list)
                    for status, items_list in metrics.items_by_status.items()
                },
                'by_priority': {
                    priority: len(items_list)
                    for priority, items_list in metrics.items_by_priority.items()
                },
                'by_assignee': {
                    assignee: len(items_list)
                    for assignee, items_list in metrics.items_by_assignee.items()
                }
            }
        }
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
