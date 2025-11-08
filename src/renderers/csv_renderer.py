"""CSV report renderer."""

import csv
from pathlib import Path
from typing import List

from src.renderers.base import Renderer
from src.models import ProjectItem, ProjectMetrics


class CSVRenderer(Renderer):
    """Renderer for generating CSV reports."""
    
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
        Render CSV report and save to file.
        
        Args:
            items: List of all project items
            metrics: Calculated project metrics
            output_path: Path to save the CSV file
            project_name: Name of the project
            owner: GitHub organization/user
            project_number: Project number
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Open file with UTF-8 BOM for Excel compatibility
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'Title',
                'Status',
                'Priority',
                'Assignees',
                'Estimate',
                'Labels',
                'URL',
                'Repository',
                'Issue Number'
            ])
            
            # Write data rows
            for item in items:
                writer.writerow([
                    item.title,
                    item.status.value,
                    item.priority.value,
                    ', '.join(item.assignees) if item.assignees else '',
                    item.estimate_hours if item.estimate_hours is not None else '',
                    ', '.join(item.labels) if item.labels else '',
                    item.url,
                    item.repository,
                    item.issue_number if item.issue_number is not None else ''
                ])
